import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials


# Googleスプレッドシートのクラス
class Gapi_Spreadsheet:
    file_name = ''
    gc = None
    workbook = None
    worksheet = None

    def __init__(self, name, sheet = None):
        self.file_name = name
        keyfile = 'data/gapi_key.json'
        with open(keyfile, 'r') as f:
            j = json.load(f)
            if not 'private_key' in j:
                j['private_key'] = os.getenv('GOOGLEAPI_PRIVATE_KEY')

        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
        self.gc = gspread.authorize(credentials)
        self.workbook = self.gc.open(self.file_name)

        if type(sheet) == str:
            self.worksheet = self.workbook.worksheet(sheet)
        elif type(sheet) == int:
            self.worksheet = self.workbook.get_worksheet(sheet)
        else:
            self.worksheet = self.workbook.sheet1

    # シートを読んで2次元のリストに格納(行列ごとに範囲をタプルで指定)
    def readrange(self, line:tuple, column:tuple):
        result = []
        insert = []

        for l in range(*line):

            for c in range(*column):
                value = self.worksheet.cell(l + 1, c + 1).value
                insert.append(value)


    def readlines(self, column = None):
        cell_data_all = self.worksheet.get_all_values()
        result = []
        insert = []
        if len(cell_data_all) < 2:
            return False
        for i, line in enumerate(cell_data_all):
            if i > 0:
                if type(column) in [tuple, list] and len(column) > 1:
                    insert = line[column[0]:column[1]]
                else:
                    insert = line
                result.append(insert)
        return result


    def writeline(self, content):
        if type(content) in [list, tuple]:
            for i, value in enumerate(content):
                self.worksheet.update_cell()
