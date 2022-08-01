# インストールした discord.py を読み込む
import discord
import datetime
import math
#import cv2
import os
import re
import numpy as np
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw

# 自分のBotのアクセストークンに置き換えてください
token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()

# Botの接頭辞を^にする
bot = commands.Bot(command_prefix="^", intents=intents, case_insensitive=True)

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    # メッセージ送信者がBotだった場合は無視する
    if ctx.author.bot:
        return
    if 'おくり' in str(ctx.content):
        await ctx.channel.send('おくりさんどれだけ性欲あるの')
        return

    if '昼' in str(ctx.content):
        await ctx.channel.send('https://lh6.googleusercontent.com/nYhbTdRBCygnfU8TCmB9BOn_OlhuORSgI1cGn9PyGGcWCqB-FCiQQqUmtJkKYT6nivh8YYkdUvDXxrkZRKr9=w1920-h961-rw')
        return

#現在時刻を送信
@bot.command()
async def now(ctx):
    date_now = datetime.datetime.now()
    date_kyotsu = datetime.datetime(2023, 1, 14)
    delta = date_kyotsu - date_now
    days_kyotsu = delta.days + 1
    await ctx.send(f'現在時刻：{date_now.strftime("%Y/%m/%d %H:%M:%S")}\n次の共通テストまであと{days_kyotsu}日です。')


#raika
@bot.command(aliases=['aaruaika'])
async def raika(ctx):
    print("debug")
    await ctx.send("Twitterをやってるときの指の動作またはスマートフォンを凝視するという行動が同じだけなのであって容姿がこのような姿であるという意味ではありません")


#fxname == 'distortion' の時に実行される関数
def distort(img, tp, par1, par2, par3, par4):
    if tp == 'wave':
        height, width = img.shape[:2]
        h1 = 0
        h2 = 0
        if par3 == 'horizontal' or par3 == 'hor':
            h1 = width
            h2 = height
        else:
            h1 = height
            h2 = width
        amp = float(par1) / 100 * h1
        freq = float(par2)

        def roop(num, min, max):
            range = max - min
            n = (num - min) // range
            val = (num - min) % range
            result = 0
            if n % 2 == 0:
                result = min + val
            else:
                result = max - val
            return result

        result = np.zeros_like(img)

        if par3 == 'horizontal' or par3 == 'hor':
            for y in range(img.shape[0]):
                for x in range(img.shape[1]):
                    for i in range(3):
                        result[y, x][i] = img[y, roop(x + math.floor(amp * math.sin(y * freq / h2)), 0, img.shape[1] - 1)][i]
        else:
            for y in range(img.shape[0]):
                for x in range(img.shape[1]):
                    for i in range(3):
                        result[y, x][i] = img[roop(y + math.floor(amp * math.sin(x * freq / h2)), 0, img.shape[0] - 1), x][i]

        return result
    return


#画像に各種エフェクトをかける
@bot.command(aliases=['fx', 'effects'])
async def effect(ctx, *params):
    fxname, par1, par2, par3, par4, par5 = params
    if ctx.message.reference is None:
        await ctx.send('加工したい画像に返信してください')
        return

    mes = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    if mes.attachments[0] is None:
        await ctx.send('返信元のメッセージにファイルが添付されていません')
        return

    await mes.attachments[0].save('img_input.png')

    mes_pros = await ctx.reply('処理中です…', mention_author=False)

    img = Image.open('img_input.png')
    if fxname == 'distortion' or fxname == 'distort':
        img_result = distort(img, par1, par2, par3, par4, par5)
    
    #処理中メッセージを削除
    await mes_pros.delete()
    if not img_result is None:
        #cv2.imwrite('temp_output.png',img_result)
        img_result.save('temp_output.png')
        await ctx.send(file=discord.File('temp_output.png'))
        os.remove('temp_input.png')
        os.remove('temp_output.png')


# Botの起動とDiscordサーバーへの接続
bot.run(token)
