import modules.img
import modules.funcs
import stable_diffusion.scripts.txt2img
import csv
#import cv2
import discord
import discord.app_commands
#import datetime
import emoji
import glob
#import librosa
#import numpy as np
import os
import random
import re
import rembg
import requests
from PIL import Image



g_models = None

REMOVEBG_APIKEY = os.getenv("REMOVEBG_APIKEY")



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
async def command_proc_effect(itrc, ctx, prompt=""):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

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
        if itrc:
            await itrc.response.send_message(embed=embed)
        elif ctx:
            await ctx.send(embed=embed)
        return

    if len(args) > 1:
        values = args[1:]
    else:
        values = []

    async with channel.typing():
        filename_input = f"data/temp/temp_input_{channel.id}.png"
        filename_output = f"data/temp/temp_output_{channel.id}.png"

        if not await modules.funcs.attachments_proc(channel, filename_input, "image"):
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
                await channel.send(embed = embed)
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
                await channel.send(embed = embed)
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

        await channel.send(file=discord.File(filename_output))

        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)



# 言葉狩り機能のオンオフ
async def command_proc_kotobagari(itrc, ctx, mode):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

    channel_id_list = []
    with open("data/csv/kotobagari.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                channel_id_list = row
    if mode:
        if not str(channel.id) in channel_id_list:
            channel_id_list.append(str(channel.id))
            text = "このチャンネルの言葉狩り機能をオンにしました。"
            if itrc:
                await itrc.response.send_message(text)
            elif ctx:
                await ctx.send(text)
        else:
            text = "このチャンネルの言葉狩り機能は既にオンです。"
            if itrc:
                await itrc.response.send_message(text)
            elif ctx:
                await ctx.send(text)
    else:
        if str(channel.id) in channel_id_list:
            channel_id_list = [id for id in channel_id_list if not id == str(channel.id)]
            text = "このチャンネルの言葉狩り機能をオフにしました。"
            if itrc:
                await itrc.response.send_message(text)
            elif ctx:
                await ctx.send(text)
        else:
            text = "このチャンネルの言葉狩り機能は既にオフです。"
            if itrc:
                await itrc.response.send_message(text)
            elif ctx:
                await ctx.send(text)
    
    with open("data/csv/kotobagari.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(channel_id_list)



# クワガタ
async def command_proc_kuwagata(itrc, ctx, kuwagata_text="クワガタ"):
    if not itrc and not ctx:
        return
    user = itrc.user if itrc else ctx.author
    result = f"{user.display_name}さん見て見て\n{kuwagata_text}～"

    if itrc:
        await itrc.response.send_message(result)
    elif ctx:
        await ctx.send(result)



# クワガタ(画像)
async def command_proc_kuwagata_img(itrc, ctx, kuwagata_text="クワガタ"):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel
    user = itrc.user if itrc else ctx.author

    async with channel.typing():
        filename_output = f"data/temp/temp_output_{channel.id}.png"
        m_img = modules.img.Mimbot_Image()
        m_img.load("data/assets/kuwagata_base.png")
        # 〇〇さん
        m_img.drawtext(
            f"{user.display_name}さん",
            (579, 22),
            fill="black",
            anchor="rt",
            fontsize=24,
            direction="ttb"
        )
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
            m_img.drawtext(
                l,
                (283 - i * 32, 18),
                fill="black",
                anchor="rt",
                fontsize=28,
                direction="ttb"
            )

        if not m_img.image is None:
            #cv2.imwrite("temp_output.png",img_result)
            m_img.image.save(filename_output)
        if itrc:
            await itrc.response.send_message(file=discord.File(filename_output))
        elif ctx:
            await ctx.send(file=discord.File(filename_output))
        if os.path.isfile(filename_output):
            os.remove(filename_output)



# おくり
async def command_proc_okuri(itrc, ctx, seiyoku="性欲", aru="ある", no="の"):
    text = f"おくりさんどれだけ{seiyoku}{aru}{no}"

    if itrc:
        await itrc.response.send_message(text)
    elif ctx:
        await ctx.send(text)



# Ping
async def command_proc_ping(itrc, ctx, client):
    # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000, 2)
    result = f"Pong! `Latency: {ping}[ms]`"
    if itrc:
        await itrc.response.send_message(result)
    elif ctx:
        await ctx.send(result)



# raika
async def command_proc_raika(itrc, ctx, n=1):
    raika_tweets = []
    # CSVファイルから読み込み
    with open("data/csv/raika_tweets.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            raika_tweets.append(row)
    
    for _ in range(n):
        raika_tweet_pickup = random.choice(raika_tweets)
        for tw in raika_tweet_pickup:
            backslash = False
            for i, ch in enumerate(tw):
                if backslash:
                    if ch == "n":
                        tw = tw[:i - 1] + "\n" + tw[i + 1:]
                    backslash = False
                if ch == "\\":
                    backslash = True
            if itrc:
                try:
                    await itrc.response.send_message(tw)
                except discord.InteractionResponded:
                    await itrc.channel.send(tw)
            elif ctx:
                await ctx.send(tw)



# 背景を透過
async def command_proc_removebg(itrc, ctx, use_removebgapi=False):
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

    if not itrc and not ctx:
        return

    channel = itrc.channel if itrc else ctx.channel

    filename_input = f"data/temp/temp_input_{channel.id}.png"
    filename_output = f"data/temp/temp_output_{channel.id}.png"

    if itrc:
        await itrc.response.defer()

    if not await modules.funcs.attachments_proc(channel, filename_input, "image"):
        return

    if use_removebgapi:
        removebgapi_remove(filename_input, filename_output)
    else:
        rembg_remove(filename_input, filename_output)
    if itrc:
        await itrc.followup.send(file=discord.File(filename_output))
    elif ctx:
        await ctx.send(file=discord.File(filename_output))

    for filename in [filename_input, filename_output]:
        if os.path.isfile(filename):
            os.remove(filename)



# 墓
async def command_proc_tomb(itrc, ctx, content=""):
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

    if itrc:
        await itrc.response.send_message(create_tomb(content))
    elif ctx:
        await ctx.send(create_tomb(content))



#Text to image(Stable Diffusion)
async def command_proc_txt2img(itrc, ctx):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

    filename_output = f"anythingv3_t2i_o_{channel.id}"
    output_dir = f"data/temp"
    result_path = f"{output_dir}/{filename_output}.png"
    def_ckpt = ""
    MODEL_DIR = "stable_diffusion/models"
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
            global g_models
            try:
                prompt = str(self.input_prompt)
                neg_prompt = str(self.input_negative_prompt)
                n_step = int(str(self.input_sampling_steps))
                width = int(str(self.input_width))
                height = int(str(self.input_height))

            except ValueError:
                await interaction.channel.send(
                    embed=discord.Embed(
                        title="エラー",
                        description="無効な入力値です。"
                    )
                )

            # インタラクションを無視
            try:
                await interaction.response.send_message("")
            except discord.errors.HTTPException:
                pass

            message = None

            if (not g_models) or (not button_continue.ckpt_ in g_models.keys()):
                message = await channel.send(
                    embed=discord.Embed(
                        title="処理中です...",
                        description="モデルの読み込み中..."
                    )
                )
                g_models = stable_diffusion.scripts.txt2img.load_model(button_continue.ckpt_, models=g_models)

            embed_creating = discord.Embed(
                title="処理中です...",
                description="生成中..."
            )

            if message:
                await message.edit(embed=embed_creating)
            else:
                message = await channel.send(embed=embed_creating)

            stable_diffusion.scripts.txt2img.txt2img_proc(
                prompt=prompt,
                negative_prompt=neg_prompt,
                filename=filename_output,
                outdir=output_dir,
                ckpt=button_continue.ckpt_,
                sampling_method=button_continue.sampling_method_,
                sampling_steps=n_step,
                width=width,
                height=height,
                models=g_models
            )
            await message.delete()

            if os.path.isfile(result_path):
                if itrc:
                    await itrc.followup.send(file=discord.File(result_path))
                elif ctx:
                    await ctx.send(file=discord.File(result_path))
                os.remove(result_path)

    if itrc:
        await itrc.response.defer()

    modal_settings = Modal_SdSettings()

    # モデルを指定するコンボボックス
    class My_Select(discord.ui.Select):
        async def callback(self, interaction):
            # インタラクションを無視
            try:
                await interaction.response.send_message("")
            except discord.errors.HTTPException:
                pass

    # "続ける"のボタン
    class Button_Continue(discord.ui.Button):
        ckpt_ = ""
        sampling_method_ = ""
        async def callback(self, interaction):
            await interaction.message.delete()
            await interaction.response.send_modal(modal_settings)
            if not list_models.values:
                self.ckpt_ = def_ckpt
            else:
                self.ckpt_ = list_models.values[0]

            if not list_sampling_methods.values:
                self.sampling_method_ = "ddim"
            else:
                self.sampling_method_ = list_sampling_methods.values[0]


    list_models = My_Select(min_values=1, max_values=1)
    models = [os.path.split(model)[1] for model in glob.glob(f"{MODEL_DIR}/*.ckpt")]
    if not models:
        await channel.send(
                    embed=discord.Embed(
                        title="エラー",
                        description="モデル(.ckpt)が見つかりません。"
                    )
                )
        return
    def_ckpt = models[0]
    for i, model in enumerate(models):
        list_models.add_option(label=model, value=model, default=i==0)

    
    list_sampling_methods = My_Select(min_values=1, max_values=1)
    list_sampling_methods.add_option(label="DDIM", value="ddim", default=True)
    list_sampling_methods.add_option(label="DPM solver", value="dpm_solver")
    list_sampling_methods.add_option(label="PLMS", value="plms")

    button_continue = Button_Continue(label="続ける")

    view = discord.ui.View()
    view.timeout = None
    view.add_item(list_models)
    view.add_item(list_sampling_methods)
    view.add_item(button_continue)

    await channel.send(
        embed=discord.Embed(title="モデル・サンプリング方法を選択："),
        view=view
    )



# ウマ娘ガチャシミュレーター
async def command_proc_uma(itrc, ctx, weights_1=100, weights_2=100, weights_3=100):
    try:
        custom_weights = [int(weights_1), int(weights_2), int(weights_3)]
        weights_sum = sum(custom_weights)
        custom_weights = [i / weights_sum * 100 for i in custom_weights]
    except:
        custom_weights = None
    await modules.funcs.send_uma(itrc, ctx, custom_weights)