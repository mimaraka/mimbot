import discord
import math
#import cv2
#herokuでcv2をimportするとエラーが出たのでとりあえずPillowで代用
import os
#import numpy as np
from discord.ext import commands
from PIL import Image
import traceback

intents = discord.Intents.all()

#Botの接頭辞を^にする
bot = commands.Bot(command_prefix="^", intents=intents, case_insensitive=True)

#起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

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
    if 'おくり' in str(ctx.content):
        await ctx.channel.send('おくりさんどれだけ性欲あるの')
        return

    if '昼' in str(ctx.content):
        await ctx.channel.send('https://p-town-admin.dmm.com/img/upload/editor/_01_%E3%83%91%E3%83%81%E3%82%B9%E3%83%AD%E6%A9%9F%E7%A8%AE%E3%83%9A%E3%83%BC%E3%82%B8/S700_%E3%83%91%E3%83%81%E3%82%B9%E3%83%AD1000%E3%81%A1%E3%82%83%E3%82%93/1221/F0002.jpg')
        return
    
#ping
@bot.command()
async def ping(ctx):
    # Ping値を秒単位で取得
    raw_ping = bot.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    await ctx.reply(f"Pong! (Latency : {ping}ms)", mention_author=False)

#raika
@bot.command(aliases=['aaruaika'])
async def raika(ctx):
    await ctx.send("Twitterをやってるときの指の動作またはスマートフォンを凝視するという行動が同じだけなのであって容姿がこのような姿であるという意味ではありません")


#fxname == 'distortion' の時に実行される関数
def distort(img, values):
    if values[0] in ['wv', 'wave']:
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


def negative(img):
    result = Image.new('RGB',img.size)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r = 255 - img.getpixel((x, y))[0]
            g = 255 - img.getpixel((x, y))[1]
            b = 255 - img.getpixel((x, y))[2]
            result.putpixel((x, y), (r, g, b))
    return result


#画像に各種エフェクトをかける
@bot.command(aliases=['fx', 'effects'])
async def effect(ctx, *params):
    if params:
        fxname = params[0]
    else:
        await ctx.send('・distortion / distort / dst：\n画像を様々な形に変形します。\n・negative / nega：\n画像のネガポジを反転します。')
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

    if fxname in ['dst', 'distort', 'distortion']:
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


# Botの起動とDiscordサーバーへの接続
token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)
