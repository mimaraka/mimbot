import modules.funcs
import bot_commands
import discord
import discord.app_commands
from discord import Interaction
from discord.ext import commands
import asyncio
import datetime
import openai
import os
import random
import re



##########################################################################
####    !!!Tokens!!!
##########################################################################
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")



COMMAND_PREFIX = "&"
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, case_insensitive=True)
tree = bot.tree
openai.api_key = OPENAI_APIKEY



##########################################################################
####    Bot Event
##########################################################################

async def change_presence():
    games = [
        "Adobe After Effects 2023",
        "Adobe Photoshop 2023",
        "Adobe Premire Pro 2023",
        "Adobe Illustrator 2023",
        "AviUtl",
        "Blender",
        "CakeWalk",
        "CLIP STUDIO PAINT PRO",
        "Cookie Clicker",
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
        "VocalShifter",
        "超将棋"
    ]
    status = [
        discord.Status.online,
        discord.Status.idle,
        discord.Status.dnd
    ]
    await bot.change_presence(
        activity=discord.Game(random.choice(games)),
        status=random.choice(status)
    )
    # 20分後に再度ステータス等を変更
    await asyncio.sleep(1200)
    await change_presence()



#起動時に動作する処理
@bot.event
async def on_ready():
    now_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print_string = f"< [ {now_string} ] Successfully logged in. >"
    print("=" * (60 + len(print_string)))
    print("-" * 30 + print_string + "-" * 30)
    print("=" * (60 + len(print_string)))

    await tree.sync()
    await change_presence()



#メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # 言葉狩り機能
    await modules.funcs.kotobagari_proc(message)

    # ChatGPT
    if bot.user.mentioned_in(message) or message.channel.type == discord.ChannelType.private:
        if message.author.bot or message.content[0] == COMMAND_PREFIX:
            return
        async with message.channel.typing():
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=re.sub(r"<@\d+>", "", message.content),
                temperature=0.9,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
            )
            result = response["choices"][0]["text"]
            if len(result) > 2048:
                result = result[:2047]
            await message.channel.send(result)




##########################################################################
####    Tree Command
##########################################################################

# BPM
@tree.command(name="bpm")
async def command_tree_bpm(itrc:Interaction):
    """
    音声のBPM値を算出します。
    (調べたい音声の近くに)/bpm
    """
    await bot_commands.bpm(itrc, None)


# 画像に各種エフェクトをかける
@tree.command(name="effect")
async def command_tree_effect(itrc:Interaction, prompt:str=""):
    """
    画像にエフェクトを適用します。
    (適用したい画像の近くに)/effect [モード] [モードごとの引数] ...
    """
    await bot_commands.effect(itrc, None, prompt=prompt)


# カニ
@tree.command(name="kani")
async def command_tree_kani(itrc:Interaction, kani_text:str="カニ"):
    """
    見て見てフラッシュさん カニファル子だよ～
    /kani ['カニ'にあたる部分の文字列]
    """
    await bot_commands.kani(itrc, None, kani_text=kani_text)


# カニ(画像)
@tree.command(name="kani_img")
async def command_tree_kani_img(itrc, kani_text:str="カニ"):
    """
    見て見てフラッシュさん カニファル子だよ～の画像版
    /kani_img ['カニ'にあたる部分の文字列]
    """
    await bot_commands.kani_img(itrc, None, kani_text=kani_text)


# 言葉狩り機能のオンオフ
@tree.command(name="kotobagari")
async def command_tree_kotobagari(itrc:Interaction, mode:bool):
    """
    送信されたチャンネルの言葉狩り機能のオン/オフを変更します。
    """
    await bot_commands.kotobagari(itrc, None, mode=mode)



# クワガタ
@tree.command(name="kuwagata")
async def command_tree_kuwagata(itrc:Interaction, kuwagata_text:str="クワガタ"):
    """
    フラッシュさん見て見て クワガタ～
    /kuwagata ['クワガタ'にあたる部分の文字列]
    """
    await bot_commands.kuwagata(itrc, None, kuwagata_text=kuwagata_text)



# クワガタ(画像)
@tree.command(name="kuwagata_img")
async def command_tree_kuwagata_img(itrc, kuwagata_text:str="クワガタ"):
    """
    フラッシュさん見て見て クワガタ～の画像版
    /kuwagata_img ['クワガタ'にあたる部分の文字列]
    """
    await bot_commands.kuwagata_img(itrc, None, kuwagata_text=kuwagata_text)



# おくり
@tree.command(name="okuri")
async def command_tree_okuri(itrc:Interaction, seiyoku:str="性欲", aru:str="ある", no:str="の"):
    """
    おくりさんどれだけ性欲あるの
    /okuri ['性欲'にあたる部分の文字列] ['ある'にあたる部分の文字列] ['の'にあたる部分の文字列]
    """
    await bot_commands.okuri(
        itrc,
        None,
        seiyoku=seiyoku,
        aru=aru,
        no=no
    )



# Ping
@tree.command(name="ping")
async def command_tree_ping(itrc:Interaction):
    """
    Ping値を取得します。
    """
    await bot_commands.ping(itrc, None, bot)



# raika
@tree.command(name="raika")
async def command_tree_raika(itrc:Interaction, n: int=1):
    """
    raikaさんのおもしろツイートガチャ
    /raika [実行したい回数]
    """
    await bot_commands.raika(itrc, None, n=n)



# 背景を透過
@tree.command(name="removebg")
async def command_tree_removebg(itrc:Interaction, use_removebgapi:bool=False):
    """
    画像の背景を透過します。
    (透過したい画像の近くに)/removebg [透過方法(オプション)]
    ・透過方法：use_removebgapiをTrueにするとremovebg APIを使って透過します。
    　　　　　　removebg APIの使用制限に達した場合はrembgが使用されます。
    """
    await bot_commands.removebg(itrc, None, use_removebgapi=use_removebgapi)



# 墓
@tree.command(name="tomb")
async def command_tree_tomb(itrc:Interaction, content:str=""):
    """
    墓を作ります。
    /tomb [文字列]
    """
    await bot_commands.tomb(itrc, None, content=content)



#Text to image(Stable Diffusion)
# @tree.command(name="txt2img")
# async def command_tree_txt2img(itrc:Interaction):
#     """
#     Stable Diffusionを用いてテキストから画像を生成します。
#     """
#     await bot_commands.txt2img(itrc, None)



# ウマ娘ガチャシミュレーター
@tree.command(name="uma")
async def command_tree_uma(itrc: Interaction, weights_1: int=79, weights_2: int=18, weights_3: int=3):
    """
    ウマ娘のガチャ(10連)をシミュレートします。
    /uma [☆1の確率の重み(オプション)] [☆2の確率の重み(オプション)] [☆3の確率の重み(オプション)] 
    """
    await bot_commands.uma(
        itrc,
        None,
        weights_1=weights_1,
        weights_2=weights_2,
        weights_3=weights_3
    )



##########################################################################
####    Bot Command
##########################################################################

# BPM
@bot.command(name="bpm")
async def command_bot_bpm(ctx):
    """
    音声のBPM値を算出します。
    (調べたい音声の近くに)&bpm
    """
    await bot_commands.bpm(None, ctx)


# 画像に各種エフェクトをかける
@bot.command(name="effect")
async def command_bot_effect(ctx, *args):
    """
    画像にエフェクトを適用します。
    (適用したい画像の近くに)&effect [モード] [モードごとの引数] ...
    """
    try:
        await bot_commands.effect(None, ctx, prompt=args[0])
    except:
        await bot_commands.effect(None, ctx)


# カニ
@bot.command(name="kani")
async def command_bot_kani(ctx, *args):
    """
    見て見てフラッシュさん カニファル子だよ～
    &kani ['カニ'にあたる部分の文字列]
    """
    if args:
        await bot_commands.kani(None, ctx, kani_text=args[0])
    else:
        await bot_commands.kani(None, ctx)


# カニ(画像)
@bot.command(name="kani_img")
async def command_bot_kani_img(ctx, *args):
    """
    見て見てフラッシュさん カニファル子だよ～の画像版
    &kani_img ['カニ'にあたる部分の文字列]
    """
    if args:
        await bot_commands.kani_img(None, ctx, kani_text=args[0])
    else:
        await bot_commands.kani_img(None, ctx)


# 言葉狩り機能のオンオフ
@bot.command(name="kotobagari")
async def command_bot_kotobagari(ctx, *args):
    """
    送信されたチャンネルの言葉狩り機能のオン/オフを変更します。
    """
    try:
        if args[0].lower() == "true":
            mode = True
        else:
            mode = False
        await bot_commands.kotobagari(None, ctx, mode=mode)
    except:
        await bot_commands.kotobagari(None, ctx, mode=False)



# クワガタ
@bot.command(name="kuwagata")
async def command_bot_kuwagata(ctx, *args):
    """
    フラッシュさん見て見て クワガタ～
    &kuwagata ['クワガタ'にあたる部分の文字列]
    """
    if args:
        await bot_commands.kuwagata(None, ctx, kuwagata_text=args[0])
    else:
        await bot_commands.kuwagata(None, ctx)



# クワガタ(画像)
@bot.command(name="kuwagata_img")
async def command_bot_kuwagata_img(ctx, *args):
    """
    フラッシュさん見て見て クワガタ～の画像版
    &kuwagata_img ['クワガタ'にあたる部分の文字列]
    """
    if args:
        await bot_commands.kuwagata_img(None, ctx, kuwagata_text=args[0])
    else:
        await bot_commands.kuwagata_img(None, ctx)



# おくり
@bot.command(name="okuri")
async def command_bot_okuri(ctx, *args):
    """
    おくりさんどれだけ性欲あるの
    &okuri ['性欲'にあたる部分の文字列] ['ある'にあたる部分の文字列] ['の'にあたる部分の文字列]
    """
    if args:
        if len(args) > 2:
            text = args
        elif len(args) == 2:
            text = [args[0], args[1], "の"]
        else:
            text = [args[0], "ある", "の"]
    else:
        text = ["性欲", "ある", "の"]
    
    await bot_commands.okuri(
        None,
        ctx,
        seiyoku=text[0],
        aru=text[1],
        no=text[2]
    )



# Ping
@bot.command(name="ping")
async def command_bot_ping(ctx):
    """
    Ping値を取得します。
    """
    await bot_commands.ping(None, ctx, bot)



# raika
@bot.command(name="raika")
async def command_bot_raika(ctx, *args):
    """
    raikaさんのおもしろツイートガチャ
    &raika [実行したい回数]
    """
    try:
        n = int(args[0])
        await bot_commands.raika(None, ctx, n=n)
    except:
        await bot_commands.raika(None, ctx)



# 背景を透過
@bot.command(name="removebg")
async def command_bot_removebg(ctx, *args):
    """
    画像の背景を透過します。
    (透過したい画像の近くに)&removebg [透過方法(オプション)]
    ・透過方法：use_removebgapiをTrueにするとremovebg APIを使って透過します。
    　　　　　　removebg APIの使用制限に達した場合はrembgが使用されます。
    """
    try:
        use_removebgapi = False
        if args[0].lower() == "true":
            await bot_commands.removebg(None, ctx, True)
    except:
        await bot_commands.removebg(None, ctx)



# 墓
@bot.command(name="tomb")
async def command_bot_tomb(ctx, *args):
    """
    墓を作ります。
    &tomb [文字列]
    """
    if args:
        await bot_commands.tomb(None, ctx, content=args[0])
    else:
        await bot_commands.tomb(None, ctx)



#Text to image(Stable Diffusion)
# @bot.command(name="txt2img")
# async def command_bot_txt2img(ctx):
#     """
#     Stable Diffusionを用いてテキストから画像を生成します。
#     """
#     await bot_commands.txt2img(None, ctx)



# ウマ娘ガチャシミュレーター
@bot.command(name="uma")
async def command_bot_uma(ctx, *args):
    """
    ウマ娘のガチャ(10連)をシミュレートします。
    &uma [☆1の確率の重み(オプション)] [☆2の確率の重み(オプション)] [☆3の確率の重み(オプション)] 
    """
    try:
        if len(args) > 2:
            custom_weights = [int(i) for i in args[:3]]
            weights_sum = sum(custom_weights)
            custom_weights = [i / weights_sum * 100 for i in custom_weights]
        else:
            custom_weights = [None, None, None]
    except:
        custom_weights = [None, None, None]
    
    await bot_commands.uma(
        None,
        ctx,
        weights_1=custom_weights[0],
        weights_2=custom_weights[1],
        weights_3=custom_weights[2]
    )



##########################################################################
####    Run
##########################################################################

# Botの起動とDiscordサーバーへの接続
bot.run(DISCORD_BOT_TOKEN)
