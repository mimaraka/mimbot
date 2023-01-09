import modules.img
import modules.funcs
import stable_diffusion.scripts.txt2img
import csv
#import cv2
import discord
import discord.app_commands
from discord import Interaction
#import datetime
import emoji
#import librosa
#import numpy as np
import os
import random
import re
import rembg
import requests
from PIL import Image

intents = discord.Intents.all()

intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

g_model = None



##########################################################################
####    Tokens
##########################################################################
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
REMOVEBG_APIKEY = os.getenv("REMOVEBG_APIKEY")



##########################################################################
####    Bot Event
##########################################################################

#起動時に動作する処理
@client.event
async def on_ready():
    print("ログイン完了")
    games = [
        "Adobe After Effects 2023",
        "Adobe Photoshop 2023",
        "Adobe Premire Pro 2023",
        "Adobe Illustrator 2023",
        "AviUtl",
        "Blender",
        "CakeWalk",
        "CLIP STUDIO PAINT PRO",
        "Cooking Simulator",
        "Crab Game",
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
    status = [
        discord.Status.online,
        discord.Status.idle,
        discord.Status.dnd
    ]
    await tree.sync()
    await client.change_presence(
        activity=discord.Game(random.choice(games)),
        status=random.choice(status)
    )

#メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # 言葉狩り機能
    await modules.funcs.kotobagari_proc(message)



##########################################################################
####    Bot Command
##########################################################################

# @client.command()
# async def bpm(itrc):
#     duration = 30
#     x_sr = 200
#     bpm_min, bpm_max = 60, 240

#     if itrc.message.reference is None:
#         await itrc.reply("適用したい音声ファイルが添付されたメッセージに返信してください", mention_author=False)
#         return

#     mes = await itrc.channel.fetch_message(itrc.message.reference.message_id)

#     if mes.attachments[0] is None:
#         await itrc.reply("返信元のメッセージにファイルが添付されていません", mention_author=False)
#         return

#     file_name = mes.attachments[0].filename

#     await mes.attachments[0].save(file_name)

#     mes_pros = await itrc.reply("処理中です…", mention_author=False)

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
#     await itrc.channel.send(f"BPM: {bpm}")
#     os.remove(file_name)



# 画像に各種エフェクトをかける
@tree.command(name="effect")
async def effect(itrc:Interaction, prompt:str):
    """
    画像にエフェクトを適用します。
    (適用したい画像の近くに)/effect [モード] [モードごとの引数] ...
    """
    args = prompt.split(",")

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
        await itrc.response.send_message(embed = embed)
        return

    if len(args) > 1:
        values = args[1:]
    else:
        values = []

    async with itrc.channel.typing():
        filename_input = f"data/temp/temp_input_{itrc.channel.id}.png"
        filename_output = f"data/temp/temp_output_{itrc.channel.id}.png"

        if not await modules.funcs.attachments_proc(itrc, filename_input, "image"):
            return

        m_img = modules.img.Mimbot_Image()
        m_img.load(filename_input)

        # ブラー
        if fxname.lower() in ["blur", "bl"]:
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
                await itrc.channel.send(embed = embed)
                return

        # 変形
        elif fxname.lower() in ["dist", "distort", "distortion"]:
            if m_img.distort(values):
                embed = discord.Embed(
                    title = "distort effect",
                    description = 
                        "**・vortex (適用量)：**\n渦ワープ\n\n"\
                        "**・wave / wav (振幅) (周期)：**\n波形ワープ"
                )
                await itrc.channel.send(embed = embed)
                return

        # エンボス
        elif fxname.lower() == "emboss":
            m_img.emboss()

        # モザイク
        elif fxname.lower() == "mosaic":
            size = int(values[0]) if values else 20
            m_img.mosaic(size)

        # ネガポジ反転
        elif fxname in ["negative", "nega"]:
            m_img.negative()

        # Pixelize
        elif fxname.lower() == "pixelize":
            size = int(values[0]) if values else 20
            m_img.pixelize(size)

        if not m_img.image is None:
            #cv2.imwrite("temp_output.png",img_result)
            m_img.image.save(filename_output)

        await itrc.channel.send(file=discord.File(filename_output))

        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)



# 言葉狩り機能のオンオフ
@tree.command(name="kotobagari")
async def kotobagari(itrc:Interaction, mode:bool):
    """
    送信されたチャンネルの言葉狩り機能のオン/オフを変更します。
    """
    channel_id_list = []
    with open("data/csv/kotobagari.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                channel_id_list = row
    if mode:
        if not str(itrc.channel.id) in channel_id_list:
            channel_id_list.append(str(itrc.channel.id))
            await itrc.response.send_message("このチャンネルの言葉狩り機能をオンにしました。")
        else:
            await itrc.response.send_message("このチャンネルの言葉狩り機能は既にオンです。")
    else:
        if str(itrc.channel.id) in channel_id_list:
            channel_id_list = [id for id in channel_id_list if not id == str(itrc.channel.id)]
            await itrc.response.send_message("このチャンネルの言葉狩り機能をオフにしました。")
        else:
            await itrc.response.send_message("このチャンネルの言葉狩り機能は既にオフです。")
    
    with open("data/csv/kotobagari.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(channel_id_list)



# クワガタ
@tree.command(name="kuwagata")
async def kuwagata(itrc:Interaction, kuwagata_text:str="クワガタ"):
    """
    フラッシュさん見て見て クワガタ～
    /kuwagata ['クワガタ'にあたる部分の文字列]
    """
    await itrc.response.send_message(f"{itrc.user.display_name}さん見て見て\n{kuwagata_text}～")



# クワガタ(画像)
@tree.command(name="kuwagata_img")
async def kuwagata_img(itrc, kuwagata_text:str="クワガタ"):
    """
    フラッシュさん見て見て クワガタ～の画像版
    /kuwagata_img ['クワガタ'にあたる部分の文字列]
    """
    async with itrc.channel.typing():
        filename_output = f"data/temp/temp_output_{itrc.channel.id}.png"
        m_img = modules.img.Mimbot_Image()
        m_img.load("data/assets/kuwagata_base.png")
        # 〇〇さん
        m_img.drawtext(f"{itrc.user.display_name}さん", (579, 22), fill="black", anchor="rt", fontsize=24, direction="ttb")
        # 〇〇～
        str_kuwagata = f"{kuwagata_text}～"
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
        await itrc.response.send_message(file=discord.File(filename_output))
        if os.path.isfile(filename_output):
            os.remove(filename_output)



# おくり
@tree.command(name="okuri")
async def okuri(itrc:Interaction, seiyoku:str="性欲", aru:str="ある", no:str="の"):
    """
    おくりさんどれだけ性欲あるの
    /okuri ['性欲'にあたる部分の文字列] ['ある'にあたる部分の文字列] ['の'にあたる部分の文字列]
    """
    await itrc.response.send_message(f"おくりさんどれだけ{seiyoku}{aru}{no}")



# Ping
@tree.command(name="ping")
async def ping(itrc:Interaction):
    """
    Ping値を取得します。
    """
    # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000, 2)
    await itrc.response.send_message(f"Pong! (Latency : {ping}[ms])")



# raika
@tree.command(name="raika")
async def raika(itrc:Interaction, n: int=1):
    """
    raikaさんのおもしろツイートガチャ
    /raika [実行したい回数]
    """
    raika_tweets = []
    # CSVファイルから読み込み
    with open("data/csv/raika_tweets.csv", encoding="utf-8") as f:
        reader = csv.reader(f, lineterminator="\n")
        for row in reader:
            raika_tweets.append(row)
    
    for _ in range(n):
        raika_tweet_pickup = random.choice(raika_tweets)
        for tw in raika_tweet_pickup:
            try:
                await itrc.response.send_message(tw)
            except:
                await itrc.channel.send(tw)



# raika_stricker
@tree.command(name="raika_stricker")
async def raika_stricker(itrc:Interaction, n:int=1):
    """
    raika stricker
    """
    raika_img_link = "https://media.discordapp.net/attachments/1002875196522381325/1062003240213942363/raika_stricker.png?width=571&height=571"
    for _ in range(n):
        try:
            await itrc.response.send_message(raika_img_link)
        except:
            await itrc.channel.send(raika_img_link)



# 背景を透過
@tree.command()
async def removebg(itrc:Interaction, use_removebgapi:bool=False):
    """
    画像の背景を透過します。
    (透過したい画像の近くに)/removebg [透過方法(オプション)]
    ・透過方法：use_removebgapiをTrueにするとremovebg APIを使って透過します。
    　　　　　　removebg APIの使用制限に達した場合はrembgが使用されます。
    """

    def rembg_remove(path_i, path_o):
        print("Using rembg...")
        image = Image.open(path_i)
        image_output = rembg.remove(image)
        image_output.save(path_o)

    def removebgapi_remove(path_i, path_o):
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": open(path_i, "rb")},
            data={"size": "auto"},
            headers={"X-Api-Key": REMOVEBG_APIKEY},
        )
        if response.status_code == requests.codes.ok:
            print("Using removebg API...")
            with open(path_o, "wb") as out:
                out.write(response.content)
        else:
            rembg_remove(path_i, path_o)

    filename_input = f"data/temp/temp_input_{itrc.channel.id}.png"
    filename_output = f"data/temp/temp_output_{itrc.channel.id}.png"

    if not await modules.funcs.attachments_proc(itrc, filename_input, "image"):
        return

    async with itrc.channel.typing():
        if use_removebgapi:
            removebgapi_remove(filename_input, filename_output)
        else:
            rembg_remove(filename_input, filename_output)
        await itrc.response.send_message(file=discord.File(filename_output))
        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)



# 墓
@tree.command(name="tomb")
async def tomb(itrc:Interaction, content:str=""):
    """
    墓を作ります。
    /tomb [文字列]
    """
    def contains_emoji(string):
        # オリジナルの絵文字を含む場合
        if re.search(r"<:.+:\d+:>", string):

            result = ["", "", ""]
            return 
        # デフォルトの絵文字を含む場合
        for char in string:
            if char in emoji.UNICODE_EMOJI:
                return True

    def create_tomb(cont = ""):
        content_ = cont.replace("\n", "")

        has_emoji = False
        tomb_top = "　　   ＿＿"
        tomb_left = ""
        tomb_right = "｜"
        tomb_bottom = "　|￣￣￣￣￣|\n　|　 |三三|　 |"
        tomb_blank = ""

        if emoji.emoji_count(content_) > 0:
            has_emoji = True
            tomb_left = "　　｜"
            tomb_blank = " 　 "
        else:
            has_emoji = False
            tomb_left = "　　 ｜"
            tomb_blank = "　"
            
        while True:
            result = f"{content_}{'の' if cont else ''}お墓\n\n{tomb_top}\n{tomb_left}{tomb_blank}{tomb_right}\n"
            # 半角英数字記号スペースを全角に変換
            # 伸ばし棒(ー)も縦に変換
            content_tmp = content_.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})).replace(" ", "　").replace("ー", "｜") if cont else "　"
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
                content_ = content_[:-1]
        return result

    await itrc.response.send_message(create_tomb(content))



#Text to image(Stable Diffusion)
@tree.command(name="sd_txt2img")
async def sd_txt2img(itrc:Interaction):
    """
    テキストから画像を生成します(Stable Diffusion)。
    """
    filename_output = f"anythingv3_t2i_o_{itrc.channel.id}"
    output_dir = f"data/temp"
    result_path = f"{output_dir}/{filename_output}.png"
    DEF_N_STEPS = 24
    DEF_WIDTH = 512
    DEF_HEIGHT = 512
    class Modal_SdSettings(discord.ui.Modal):
        def __init__(self):
            super().__init__(title="Stable Diffusionの設定", timeout=None)
            # プロンプト
            self.input_prompt = discord.ui.TextInput(
                label="プロンプト",
                required=True,
                style=discord.TextStyle.paragraph
            )

                # ネガティブプロンプト
            self.input_negative_prompt = discord.ui.TextInput(
                label="ネガティブプロンプト",
                required=False,
                style=discord.TextStyle.paragraph
            )

            # サンプリングのステップ数
            self.input_sampling_steps = discord.ui.TextInput(
                label="サンプリングのステップ数",
                style=discord.TextStyle.short,
                default=f"{DEF_N_STEPS}"
            )

            # 画像の幅
            self.input_width = discord.ui.TextInput(
                label="画像の幅",
                style=discord.TextStyle.short,
                default=f"{DEF_WIDTH}"
            )

            # 画像の高さ
            self.input_height = discord.ui.TextInput(
                label="画像の高さ",
                style=discord.TextStyle.short,
                default=f"{DEF_HEIGHT}"
            )

            self.add_item(self.input_prompt)
            self.add_item(self.input_negative_prompt)
            self.add_item(self.input_sampling_steps)
            self.add_item(self.input_width)
            self.add_item(self.input_height)

        async def on_submit(self, interaction):
            global g_model
            try:
                prompt = str(self.input_prompt)
                neg_prompt = str(self.input_negative_prompt)
                n_step = int(str(self.input_sampling_steps))
                width = int(str(self.input_width))
                height = int(str(self.input_height))

                # 無視
                try:
                    await interaction.response.send_message("")
                except:
                    pass

                if not g_model:
                    message = await itrc.channel.send(
                        embed=discord.Embed(
                            title="処理中です...",
                            description="モデルの読み込み中..."
                        )
                    )
                    g_model = stable_diffusion.scripts.txt2img.load_model_from_config()
                    await message.delete()

                message = await itrc.channel.send(
                    embed=discord.Embed(
                        title="処理中です...",
                        description="生成中..."
                    )
                )
                stable_diffusion.scripts.txt2img.anything_txt2img(
                    prompt=prompt,
                    negative_prompt=neg_prompt,
                    filename=filename_output,
                    outdir=output_dir,
                    width=width,
                    height=height,
                    sampling_steps=n_step,
                    model=g_model
                )
                await message.delete()

                if os.path.isfile(result_path):
                    await itrc.channel.send(content=f"<@{itrc.user.id}>", file=discord.File(result_path))
                    os.remove(result_path)

            except:
                await interaction.channel.send(
                    embed=discord.Embed(
                        title="エラー",
                        description="無効な入力値です。"
                    )
                )

    modal_settings = Modal_SdSettings()

    # サンプリング方法を指定するコンボボックス
    class Select_Sampling_Method(discord.ui.Select):
        async def callback(self, interaction):
            # 無視
            try:
                await interaction.response.send_message("")
            except:
                pass

    # "続ける"のボタン
    class Button_Continue(discord.ui.Button):
        async def callback(self, interaction):
            await interaction.message.delete()
            await interaction.response.send_modal(modal_settings)

    
    list_sampling_method = Select_Sampling_Method(min_values=1, max_values=1)
    list_sampling_method.add_option(label="DDIM", value="ddim", default=True)
    list_sampling_method.add_option(label="DPM solver", value="dpm_solver")
    list_sampling_method.add_option(label="PLMS", value="plms")

    button_continue = Button_Continue(label="続ける")

    view = discord.ui.View()
    view.timeout = None
    view.add_item(list_sampling_method)
    view.add_item(button_continue)

    await itrc.response.send_message(
        embed=discord.Embed(title="サンプリング方法を選択："),
        view=view
    )



# ウマ娘ガチャシミュレーター
@tree.command()
async def uma(itrc: Interaction, weights_1: int=100, weights_2: int=100, weights_3: int=100):
    """
    ウマ娘のガチャ(10連)をシミュレートします。
    /uma [☆1の確率の重み(オプション)] [☆2の確率の重み(オプション)] [☆3の確率の重み(オプション)] 
    """
    try:
        custom_weights = [int(weights_1), int(weights_2), int(weights_3)]
        weights_sum = sum(custom_weights)
        custom_weights = [i / weights_sum * 100 for i in custom_weights]
    except:
        custom_weights = None
    await modules.funcs.send_uma(itrc, custom_weights)



##########################################################################
####    Run
##########################################################################

# Botの起動とDiscordサーバーへの接続
client.run(DISCORD_BOT_TOKEN)
