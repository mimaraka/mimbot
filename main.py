import modules.img
import modules.funcs
import csv
#import cv2
import discord
#import datetime
import emoji
#import librosa
#import numpy as np
import os
import random
import re
import requests
import traceback
from discord.ext import commands
from PIL import Image
from rembg import remove

intents = discord.Intents.all()

#Botの接頭辞を"^"にする
bot = commands.Bot(command_prefix="^", intents=intents, case_insensitive=True)



##########################################################################
####    Bot Event
##########################################################################

#起動時に動作する処理
@bot.event
async def on_ready():
    print("ログイン完了。")
    game_list = [
        "Adobe After Effects 2022",
        "Adobe Photoshop 2022",
        "Adobe Premire Pro 2022",
        "Adobe Illustrator 2022",
        "AviUtl",
        "Blender",
        "CakeWalk",
        "CLIP STUDIO PAINT PRO",
        "Cooking Simulator",
        "FallGuys",
        "LDPlayer",
        "Maxon Cinema 4D",
        "Minecraft",
        "NoxPlayer",
        "REAPER",
        "Splatoon 3",
        "Terraria",
        "Unrailed!",
        "Visual Studio 2022",
        "Visual Studio Code",
        "VocalShifter"
    ]
    await bot.change_presence(activity=discord.Game(random.choice(game_list)))


#エラー発生時に動作する処理
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = "".join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send("```" + error_msg + "```")


#メッセージ受信時に動作する処理
@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    # 言葉狩り機能
    await modules.funcs.kotobagari_proc(ctx)


# @bot.event
# async def on_interaction(interaction):
#     await modules.funcs.send_uma(interaction.channel, interaction.user)



##########################################################################
####    Bot Command
##########################################################################

# @bot.command()
# async def bpm(ctx):
#     duration = 30
#     x_sr = 200
#     bpm_min, bpm_max = 60, 240

#     if ctx.message.reference is None:
#         await ctx.reply("適用したい音声ファイルが添付されたメッセージに返信してください", mention_author=False)
#         return

#     mes = await ctx.channel.fetch_message(ctx.message.reference.message_id)

#     if mes.attachments[0] is None:
#         await ctx.reply("返信元のメッセージにファイルが添付されていません", mention_author=False)
#         return

#     file_name = mes.attachments[0].filename

#     await mes.attachments[0].save(file_name)

#     mes_pros = await ctx.reply("処理中です…", mention_author=False)

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

#     # BPM値を算出
#     bpm = np.argmax(x_bpm)

#     await mes_pros.delete()
#     await ctx.send(f"BPM: {bpm}")
#     os.remove(file_name)


# 画像に各種エフェクトをかける
@bot.command(aliases=["fx", "effects"])
async def effect(ctx, *args):
    if args:
        fxname = args[0]
    else:
        embed = discord.Embed(
            title = "effect command",
            description = 
                "**・blur (ブラーの種類)**\n画像にブラーを適用します。\n\n"\
                "**・distortion / distort / dist (変形の種類)：**\n画像を様々な形に変形します。\n\n"\
                "**・mosaic (サイズ)：**\n画像にモザイクを適用します。\n\n"\
                "**・negative / nega：**\n画像のネガポジを反転します。\n\n"\
                "**・pixelize (サイズ)：**\n画像をドット絵風の見た目にします。"
        )
        await ctx.send(embed = embed)
        return

    if len(args) > 1:
        values = args[1:]
    else:
        values = []

    async with ctx.typing():
        filename_input = f"data/temp/temp_input_{ctx.channel.id}.png"
        filename_output = f"data/temp/temp_output_{ctx.channel.id}.png"

        if not await modules.funcs.attachments_proc(ctx, filename_input, "image"):
            return

        m_img = modules.img.Mimbot_Image()
        m_img.load(filename_input)

        # ブラー
        if fxname in ["blur", "bl"]:
            if m_img.blur(values):
                embed = discord.Embed(
                    title = "blur effect",
                    description = 
                        "**・box (サイズ)：**\nボックスブラー\n\n"\
                        "**・gaussian (サイズ)：**\nガウシアンブラー\n\n"\
                        "**・median (サイズ)：**\nメディアンブラー\n\n"\
                        "**・maximun / max (サイズ)：**\n最大値フィルタ\n\n"\
                        "**・minimum / min (サイズ)：**\n最小値フィルタ\n\n"\
                        "**・rank (サイズ) (ランク)：**\nランクフィルタ"
                )
                await ctx.send(embed = embed)
                return

        # 変形
        elif fxname in ["dist", "distort", "distortion"]:
            if m_img.distort(values):
                embed = discord.Embed(
                    title = "distort effect",
                    description = 
                        "**・vortex (適用量)：**\n渦ワープ\n\n"\
                        "**・wave / wav (振幅) (周期)：**\n波形ワープ"
                )
                await ctx.send(embed = embed)
                return

        # エンボス
        elif fxname == "emboss":
            m_img.emboss()

        # モザイク
        elif fxname == "mosaic":
            size = int(values[0]) if values else 20
            m_img.mosaic(size)

        # ネガポジ反転
        elif fxname in ["negative", "nega"]:
            m_img.negative()

        # Pixelize
        elif fxname == "pixelize":
            size = int(values[0]) if values else 20
            m_img.pixelize(size)

        if not m_img.image is None:
            #cv2.imwrite("temp_output.png",img_result)
            m_img.image.save(filename_output)

        await ctx.send(file=discord.File(filename_output))

        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)


# 言葉狩り機能のオンオフ
@bot.command(aliases=["ktbgr"])
async def kotobagari(ctx, *arg):
    if arg:
        kotoba_onoff = arg[0]
        channel_id_list = []
        with open("data/kotobagari.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                channel_id_list = row
            
        if kotoba_onoff in ["on", "ON"] and str(ctx.channel.id) in channel_id_list:
            channel_id_list = [id for id in channel_id_list if not id == str(ctx.channel.id)]
            await ctx.send("このチャンネルの言葉狩り機能をオンにしました。")
        elif kotoba_onoff in ["off", "OFF"] and not str(ctx.channel.id) in channel_id_list:
            channel_id_list.append(str(ctx.channel.id))
            await ctx.send("このチャンネルの言葉狩り機能を一時的にオフにしました。")
        
        with open("data/kotobagari.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(channel_id_list)


# クワガタ
@bot.command(aliases=["kwgt"])
async def kuwagata(ctx, *args):
    async def send_kuwagata(text):
        await ctx.send(f"{ctx.author.display_name}さん見て見て\n{text}～")

    if not args:
        await send_kuwagata("クワガタ")
        return
    for el in args:
        await send_kuwagata(el)


# クワガタ(画像)
@bot.command(aliases=["kwgt_img"])
async def kuwagata_img(ctx, *args):
    async def send_kuwagata_img(text):
        filename_output = f"data/temp/temp_output_{ctx.channel.id}.png"
        m_img = modules.img.Mimbot_Image()
        m_img.load("data/assets/kuwagata_base.png")
        # 〇〇さん
        m_img.drawtext(f"{ctx.author.display_name}さん", (579, 22), fill="black", anchor="rt", fontsize=24, direction="ttb")
        # 〇〇～
        str_kuwagata = f"{text}～"
        lines = []
        line = ""
        for i, char in enumerate(str_kuwagata):
            if i % 29 == 0 and i != 0:
                lines.append(line)
                line = ""
            line += char
            if i == len(str_kuwagata) - 1:
                lines.append(line)
        for i, l in enumerate(lines):
            m_img.drawtext(l, (283 - i * 32, 18), fill="black", anchor="rt", fontsize=28, direction="ttb")

        if not m_img.image is None:
            #cv2.imwrite("temp_output.png",img_result)
            m_img.image.save(filename_output)
        await ctx.send(file=discord.File(filename_output))
        if os.path.isfile(filename_output):
            os.remove(filename_output)

    async with ctx.typing():
        if not args:
            await send_kuwagata_img("クワガタ")
            return
        for el in args:
            await send_kuwagata_img(el)


# okuri
@bot.command()
async def okuri(ctx, *arg):
    if arg:
        if len(arg) > 2:
            text = arg
        elif len(arg) == 2:
            text = [arg[0], arg[1], "の"]
        else:
            text = [arg[0], "ある", "の"]
    else:
        text = ["性欲", "ある", "の"]
    await ctx.send(f"おくりさんどれだけ{text[0]}{text[1]}{text[2]}")


# ping
@bot.command()
async def ping(ctx):
    # Ping値を秒単位で取得
    raw_ping = bot.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000, 2)
    await ctx.reply(f"Pong! (Latency : {ping}[ms])", mention_author=False)


# raika
@bot.command(aliases=["aaruaika"])
async def raika(ctx, *arg):
    raika_tweets = []
    # CSVファイルから読み込み
    with open("data/csv/raika_tweets.csv") as f:
        reader = csv.reader(f, lineterminator="\n")
        for row in reader:
            raika_tweets.append(row)

    n = int(arg[0]) if arg else 1
    for _ in range(n):
        raika_tweet_pickup = random.choice(raika_tweets)
        for tw in raika_tweet_pickup:
            await ctx.send(tw)


# 背景を除去(RemoveBG)
@bot.command()
async def removebg(ctx):
    removebg_apikey = os.getenv("REMOVEBG_APIKEY")

    filename_input = f"data/temp/temp_input_{ctx.channel.id}.png"
    filename_output = f"data/temp/temp_output_{ctx.channel.id}.png"

    if not await modules.funcs.attachments_proc(ctx, filename_input, "image"):
        return

    async with ctx.typing():
        #RemoveBgAPI
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": open(filename_input, "rb")},
            data={"size": "auto"},
            headers={"X-Api-Key": removebg_apikey},
        )

        if response.status_code == requests.codes.ok:
            with open(filename_output, "wb") as out:
                out.write(response.content)
                await ctx.send(file=discord.File(filename_output))
                for filename in [filename_input, filename_output]:
                    if os.path.isfile(filename):
                        os.remove(filename)
        else:
            await ctx.send(f"```Error:{response.status_code} {response.text}```")


# rembg
@bot.command()
async def removebg2(ctx):
    filename_input = f"data/temp/temp_input_{ctx.channel.id}.png"
    filename_output = f"data/temp/temp_output_{ctx.channel.id}.png"

    if not await modules.funcs.attachments_proc(ctx, filename_input, "image"):
        return
    
    async with ctx.typing():
        image = Image.open(filename_input)
        image_output = remove(image)
        image_output.save(filename_output)
        await ctx.send(file=discord.File(filename_output))
        
        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)



# 墓
@bot.command(aliases=["grave"])
async def tomb(ctx, *args):
    def contains_emoji(string):
        # オリジナルの絵文字を含む場合
        if re.search(r"<:.+:\d+:>", string):

            result = ["dslfajdlkj", "<:asdfa:234234:>", "kdlsjf"]
            return 
        # デフォルトの絵文字を含む場合
        for chat in string:
            if char in emoji.UNICODE_EMOJI:
                return True
    
    if args:
        for content in args:
            content = content.replace("\n", "")

            has_emoji = False
            tomb_top = "　　   ＿＿"
            tomb_left = ""
            tomb_right = "｜"
            tomb_bottom = "　|￣￣￣￣￣|\n　|　 |三三|　 |"
            tomb_blank = ""

            if emoji.emoji_count(content) > 0:
                has_emoji = True
                tomb_left = "　　｜"
                tomb_blank = " 　 "
            else:
                has_emoji = False
                tomb_left = "　　 ｜"
                tomb_blank = "　"
                
            while True:
                result = f"{content}のお墓\n\n{tomb_top}\n{tomb_left}{tomb_blank}{tomb_right}\n"
                # 半角英数字記号スペースを全角に変換
                # 伸ばし棒(ー)も縦に変換
                content_tmp = content.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})).replace(" ", "　").replace("ー", "｜")
                for char in content_tmp:
                    if has_emoji:
                        if emoji.is_emoji(char):
                            add = f"{tomb_left}{char}{tomb_right}\n"
                        else:
                            add = f"{tomb_left} {char} {tomb_right}\n"
                    else:
                        add = f"{tomb_left}{char}{tomb_right}\n"
                    result += add
                result += f"{tomb_left}{tomb_blank}{tomb_right}\n{tomb_bottom}"

                if len(result) <= 2000:
                    break
                else:
                    content = content[:-1]
    
            await ctx.send(result)



@bot.command()
async def debug(ctx, *args):
    await ctx.send('```' + args[0] + '```')


@bot.command()
async def isemoji(ctx, *args):
    await ctx.send(emoji.is_emoji(args[0]))
    await ctx.send(emoji.emoji_count(args[0]))



# ウマ娘ガチャシミュレーター
@bot.command()
async def uma(ctx, *args):
    try:
        if len(args) > 2:
            custom_weights = [int(i) for i in args[:3]]
            weights_sum = sum(custom_weights)
            custom_weights = [i / weights_sum * 100 for i in custom_weights]
        else:
            custom_weights = None
    except:
        custom_weights = None
    await modules.funcs.send_uma(ctx.channel, ctx.author, custom_weights)



##########################################################################
####    Run
##########################################################################

# Botの起動とDiscordサーバーへの接続
token = os.getenv("DISCORD_BOT_TOKEN")
bot.run(token)
