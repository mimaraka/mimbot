from discord.ext import commands
#import cv2
#herokuでcv2をimportするとエラーが出たのでとりあえずPillowで代用
import discord
from PIL import Image
#import librosa
import math
import numpy as np
import os
import random
import re
import requests
import traceback

intents = discord.Intents.all()

#Botの接頭辞を"^"にする
bot = commands.Bot(command_prefix='^', intents=intents, case_insensitive=True)



##########################################################################
####    Bot Event
##########################################################################

#起動時に動作する処理
@bot.event
async def on_ready():
    print('ログイン完了')


#エラー発生時に動作する処理
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


#メッセージ受信時に動作する処理
@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    # メッセージ送信者がBotだった場合は無視する
    if ctx.author.bot:
        return

    if 'あつい' in str(ctx.content) or '暑' in str(ctx.content):
        await ctx.channel.send('https://cdn.discordapp.com/attachments/1002875196522381325/1003853181777887282/temp_output.png')

    if re.search(r"(お|オ).{,3}(く|ク).{,3}(り|リ)", str(ctx.content)):
        await ctx.channel.send('おくりさんどれだけ性欲あるの')

    if 'ごきぶり' in str(ctx.content) or 'ゴキブリ' in str(ctx.content):
        await ctx.channel.send('フラッシュさん見て見て\nゴキブリ～')

    if 'ひる' in str(ctx.content) or '昼' in str(ctx.content):
        images = [
            'https://cdn.discordapp.com/attachments/1002875196522381325/1003699645458944011/FTakxQUaIAAoyn3CUnetnoise_scaleLevel2x4.000000.png',
            'https://cdn.discordapp.com/attachments/1002875196522381325/1008245051077443664/FZmJ06EUIAAcZNi.jpg'
        ]
        image_pickup = random.choice(images)
        await ctx.channel.send(image_pickup)



##########################################################################
####    Bot Command
##########################################################################

# @bot.command()
# async def bpm(ctx):
#     duration = 30
#     x_sr = 200
#     bpm_min, bpm_max = 60, 240

#     if ctx.message.reference is None:
#         await ctx.reply('適用したい音声ファイルが添付されたメッセージに返信してください', mention_author=False)
#         return

#     mes = await ctx.channel.fetch_message(ctx.message.reference.message_id)

#     if mes.attachments[0] is None:
#         await ctx.reply('返信元のメッセージにファイルが添付されていません', mention_author=False)
#         return

#     file_name = mes.attachments[0].filename

#     await mes.attachments[0].save(file_name)

#     mes_pros = await ctx.reply('処理中です…', mention_author=False)

#     # 楽曲の信号を読み込む
#     y, sr = librosa.load(file_name, offset=38, duration=duration, mono=True)

#     # ビート検出用信号の生成
#     # リサンプリング & パワー信号の抽出
#     x = np.abs(librosa.resample(y, sr, x_sr)) ** 2
#     x_len = len(x)

#     # 各BPMに対応する複素正弦波行列を生成
#     M = np.zeros((bpm_max, x_len), dtype=np.complex)
#     for bpm in range(bpm_min, bpm_max): 
#         thete = 2 * np.pi * (bpm/60) * (np.arange(0, x_len) / x_sr)
#         M[bpm] = np.exp(-1j * thete)

#     # 各BPMとのマッチング度合い計算
#     #（複素正弦波行列とビート検出用信号との内積）
#     x_bpm = np.abs(np.dot(M, x))

#     # BPM　を算出
#     bpm = np.argmax(x_bpm)

#     await mes_pros.delete()
#     await ctx.send(f'BPM: {bpm}')
#     os.remove(file_name)


#画像に各種エフェクトをかける
@bot.command(aliases=['fx', 'effects'])
async def effect(ctx, *params):
    #fxname == 'distortion' の時に実行される関数
    def distort(img, values):
        if values[0] in ['wav', 'wave']:
            #height, width = img.shape[:2]
            width, height = img.size
            h1 = 0
            h2 = 0
            if len(values) > 3 and values[3] in ['hor', 'horizontal']:
                h1 = width
                h2 = height
            else:
                h1 = height
                h2 = width
            amp = float(values[1]) / 100 * h1
            freq = float(values[2])

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

            #result = np.zeros_like(img)
            result = Image.new('RGB',img.size)

            #OpenCVはsizeではなくshape
            if len(values) > 3 and values[3] in ['hor', 'horizontal']:
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        #for i in range(3):
                            #result[y, x][i] = img[y, roop(x + math.floor(amp * math.sin(y * freq / h2)), 0, img.shape[1] - 1)][i]
                        result.putpixel((x, y), tuple(img.getpixel((roop(x + math.floor(amp * math.sin(y * freq / h2)), 0, img.size[0] - 1), y))))
            else:
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        #for i in range(3):
                            #result[y, x][i] = img[roop(y + math.floor(amp * math.sin(x * freq / h2)), 0, img.shape[0] - 1), x][i]
                        result.putpixel((x, y), tuple(img.getpixel((x, roop(y + math.floor(amp * math.sin(x * freq / h2)), 0, img.size[1] - 1)))))
            return result
        return

    #fxname == 'negative' の時に実行される関数
    def negative(img):
        result = Image.new('RGB',img.size)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r = 255 - img.getpixel((x, y))[0]
                g = 255 - img.getpixel((x, y))[1]
                b = 255 - img.getpixel((x, y))[2]
                result.putpixel((x, y), (r, g, b))
        return result
    
    if params:
        fxname = params[0]
    else:
        await ctx.send('・distortion / distort / dist：\n画像を様々な形に変形します。\n・negative / nega：\n画像のネガポジを反転します。')
        return
    if len(params) > 1:
        values = params[1:]
    
    if ctx.message.reference is None:
        await ctx.reply('加工したい画像に返信してください', mention_author=False)
        return

    mes = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    if mes.attachments[0] is None:
        await ctx.reply('返信元のメッセージにファイルが添付されていません', mention_author=False)
        return

    await mes.attachments[0].save('temp_input.png')

    mes_pros = await ctx.reply('処理中です…', mention_author=False)

    img = Image.open('temp_input.png')

    if fxname in ['dist', 'distort', 'distortion']:
        img_result = distort(img, values)
    elif fxname in ['negative', 'nega']:
        img_result = negative(img)
    
    #処理中メッセージを削除
    await mes_pros.delete()
    if not img_result is None:
        #cv2.imwrite('temp_output.png',img_result)
        img_result.save('temp_output.png')
        await ctx.send(file=discord.File('temp_output.png'))
        os.remove('temp_input.png')
        os.remove('temp_output.png')


#クワガタ
@bot.command(aliases=['kwgt'])
async def kuwagata(ctx, *arg):
    async def send_kuwagata(text):
        await ctx.send(f"{ctx.author.display_name}さん見て見て\n{text}～")

    if not arg:
        await send_kuwagata('クワガタ')
        return
    for el in arg:
        await send_kuwagata(el)


#ping
@bot.command()
async def ping(ctx):
    # Ping値を秒単位で取得
    raw_ping = bot.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000, 2)
    await ctx.reply(f"Pong! (Latency : {ping}ms)", mention_author=False)


#raika
@bot.command(aliases=['aaruaika'])
async def raika(ctx):
    raika_tweets = [
        ["Twitterをやってるときの指の動作またはスマートフォンを凝視するという行動が同じだけなのであって容姿がこのような姿であるという意味ではありません"],
        ["はぁ、どちら様ですか？"],
        ["帽子どかしたら脳があってしかもそれが糊", "https://pbs.twimg.com/media/FM_1hGoVUAIdiGW?format=jpg&name=large"],
        ["https://pbs.twimg.com/media/FPL_nzGVUAkVzmg?format=png&name=small"],
        ["アニメアイコン洗った？"],
        ["今脳内で生成されてる音でも書き起すかドンパッドンドドンパッチュチュンチュンチュチュンチュンドンパパッパッドドッパッドドドドドパッ"],
        ['私は " ゴキブリ " に家賃を払わせることで年収 " 1500万円 " を稼ぎました。\n詳細はこちらから→'],
        ['セイキン夫婦がガチでハマってるお菓子ランキング2022'],
        ['初めてなんだけど…下手だったらごめんねｼﾞｭｯﾎﾞｼﾞｭﾎﾞｼﾞｭﾙﾙﾙｽﾞﾎﾞﾎﾞﾎﾞｼﾞｭﾎﾞﾁﾞｭｳｳｳｯﾊﾟｼﾞｭﾎﾞﾎﾞﾎﾞﾎﾞﾎﾞﾎﾞﾎﾞｼﾞｭﾙﾙﾙﾙﾙﾙﾙｼﾞｭｯﾊﾟｧ!ごっくん…'],
        ['それでは恒例イモトを探せ'],
        ['から揚げ専用ペプシをから揚げ食べずに飲んでしまいました'],
        ['猫耳','https://pbs.twimg.com/media/FUpC6h8UcAA8wrg?format=jpg&name=240x240'],
        ['チーズ牛丼食べてから記憶ない'],
        ['蚊なのか蚊じゃないのかよく分からない虫に小一時間ぐらい弄ばれてるんだけどよく考えたら虫にもちゃんと呼び名があるはずだからよく分からない虫って書くのは良いことじゃないのかもしれない'],
        ['電音部  新エリア', 'https://pbs.twimg.com/media/FTdLSTIUsAA4bzb?format=jpg&name=small'],
        ['水族館で一生魚だけ見ててください'],
        ['湿原で失言'],
        ['https://pbs.twimg.com/media/FSWhxg6VEAEBJXh?format=jpg&name=small'],
        ['シコルドあるあるアラッー！のところで白パーティクル射精'],
        ['※本ビデオ本編4章後半にイキスギあり'],
        ['家賃と電気代割ってみた！'],
        ['لا أستطيع التفكير في الأمر بالفطرة السليمة ، ولا يمكنني التفكير فيه بالفطرة السليمة ، ولا يمكنني التفكير فيه بالفطرة السليمة ، ولا يمكنني التفكير فيه بالفطرة السليمة لا أستطيع التفكير في الأمر بالفطرة السليمة لا يمكنني التفكير فيه بالفطرة السليمة لا يمكن سليم لا يمكن تصوره بالحس', 'https://pbs.twimg.com/media/FNlO4ivVcAEaFaP?format=jpg&name=small']
    ]
    raika_tweet_pickup = random.choice(raika_tweets)
    for tw in raika_tweet_pickup:
        await ctx.send(tw)


#removebg
@bot.command()
async def removebg(ctx):
    removebg_apikey = os.getenv('REMOVEBG_APIKEY')

    if ctx.message.reference is None:
        await ctx.reply('加工したい画像に返信してください', mention_author=False)
        return

    mes = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    if mes.attachments[0] is None:
        await ctx.reply('返信元のメッセージにファイルが添付されていません', mention_author=False)
        return

    await mes.attachments[0].save('temp_removebg_input.png')

    mes_pros = await ctx.reply('処理中です…', mention_author=False)

    # RemoveBgAPI
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open('temp_removebg_input.png', 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': removebg_apikey},
    )
    await mes_pros.delete()

    if response.status_code == requests.codes.ok:
        with open('removebg_temp_output.png', 'wb') as out:
            out.write(response.content)
            await ctx.send(file=discord.File('removebg_temp_output.png'))
            os.remove('temp_removebg_input.png')
            os.remove('removebg_temp_output.png')
    else:
        await ctx.send(f"Error:{response.status_code} {response.text}")



##########################################################################
####    Run
##########################################################################

# Botの起動とDiscordサーバーへの接続
token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)