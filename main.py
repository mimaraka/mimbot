import modules.img
import modules.funcs
import modules.img_utils as img_utils
import csv
import discord
import emoji
import os
import random
import re
import requests
import traceback
from discord.ext import commands
from PIL import Image

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='^', intents=intents, case_insensitive=True)



##########################################################################
####    Bot Event
##########################################################################
@bot.event
async def on_ready():
    print('ログイン完了。')
    game_list = [
        'Adobe After Effects 2022',
        'Adobe Photoshop 2022',
        'Adobe Illustrator 2022',
        'AviUtl',
        'Blender',
        'CakeWalk',
        'CLIP STUDIO PAINT PRO',
        'Cooking Simulator',
        'FallGuys',
        'Maxon Cinema 4D',
        'REAPER',
        'Visual Studio 2022',
        'Visual Studio Code',
        'VocalShifter'
    ]
    await bot.change_presence(activity=discord.Game(random.choice(game_list)))


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send('```' + error_msg + '```')


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    await modules.funcs.kotobagari_proc(ctx)



##########################################################################
####    Bot Command
##########################################################################
@bot.command(aliases=['fx', 'effects'])
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
        filename_input = f'data/temp/temp_input_{ctx.channel.id}.png'
        filename_output = f'data/temp/temp_output_{ctx.channel.id}.png'

        if not await modules.funcs.attachments_proc(ctx, filename_input, 'image'):
            return

        m_img = modules.img.Mimbot_Image()
        m_img.load(filename_input)

        if fxname in ['blur', 'bl']:
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

        elif fxname in ['dist', 'distort', 'distortion']:
            if m_img.distort(values):
                embed = discord.Embed(
                    title = "distort effect",
                    description = 
                        "**・vortex (適用量)：**\n渦ワープ\n\n"\
                        "**・wave / wav (振幅) (周期)：**\n波形ワープ"
                )
                await ctx.send(embed = embed)
                return

        elif fxname == 'emboss':
            m_img.emboss()

        elif fxname == 'mosaic':
            size = values[0] if values else 20
            m_img.mosaic(size)

        elif fxname in ['negative', 'nega']:
            m_img.negative()

        elif fxname == 'pixelize':
            size = values[0] if values else 20
            m_img.pixelize(size)

        if not m_img.image is None:
            m_img.image.save(filename_output)

        await ctx.send(file=discord.File(filename_output))

        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)


@bot.command(aliases=['ktbgr'])
async def kotobagari(ctx, *arg):
    if arg:
        kotoba_onoff = arg[0]
        channel_id_list = []
        with open('data/kotobagari.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                channel_id_list = row
            
        if kotoba_onoff in ['on', 'ON'] and str(ctx.channel.id) in channel_id_list:
            channel_id_list = [id for id in channel_id_list if not id == str(ctx.channel.id)]
            await ctx.send('このチャンネルの言葉狩り機能をオンにしました。')
        elif kotoba_onoff in ['off', 'OFF'] and not str(ctx.channel.id) in channel_id_list:
            channel_id_list.append(str(ctx.channel.id))
            await ctx.send('このチャンネルの言葉狩り機能を一時的にオフにしました。')
        
        with open('data/kotobagari.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(channel_id_list)


@bot.command(aliases=['kwgt'])
async def kuwagata(ctx, *args):
    async def send_kuwagata(text):
        await ctx.send(f"{ctx.author.display_name}さん見て見て\n{text}～")

    if not args:
        await send_kuwagata('クワガタ')
        return
    for el in args:
        await send_kuwagata(el)


@bot.command(aliases=['kwgt_img'])
async def kuwagata_img(ctx, *args):
    async def send_kuwagata_img(text):
        filename_output = f'data/temp/temp_output_{ctx.channel.id}.png'
        m_img = modules.img.Mimbot_Image()
        m_img.load('data/assets/kuwagata_base.png')
        m_img.drawtext(f'{ctx.author.display_name}さん', (579, 22), fill='black', anchor='rt', fontsize=24, direction='ttb')
        str_kuwagata = f'{text}～'
        lines = []
        line = ''
        for i, char in enumerate(str_kuwagata):
            if i % 29 == 0 and i != 0:
                lines.append(line)
                line = ''
            line += char
            if i == len(str_kuwagata) - 1:
                lines.append(line)
        for i, l in enumerate(lines):
            m_img.drawtext(l, (283 - i * 32, 18), fill='black', anchor='rt', fontsize=28, direction='ttb')

        if not m_img.image is None:
            m_img.image.save(filename_output)
        await ctx.send(file=discord.File(filename_output))
        if os.path.isfile(filename_output):
            os.remove(filename_output)

    async with ctx.typing():
        if not args:
            await send_kuwagata_img('クワガタ')
            return
        for el in args:
            await send_kuwagata_img(el)


@bot.command()
async def okuri(ctx, *arg):
    if arg:
        if len(arg) > 2:
            text = arg
        elif len(arg) == 2:
            text = [arg[0], arg[1], 'の']
        else:
            text = [arg[0], 'ある', 'の']
    else:
        text = ['性欲', 'ある', 'の']
    await ctx.send(f'おくりさんどれだけ{text[0]}{text[1]}{text[2]}')


@bot.command()
async def ping(ctx):
    raw_ping = bot.latency
    ping = round(raw_ping * 1000, 2)
    await ctx.reply(f"Pong! (Latency : {ping}[ms])", mention_author=False)


@bot.command(aliases=['aaruaika'])
async def raika(ctx, *arg):
    raika_tweets = []
    with open('data/csv/raika_tweets.csv') as f:
        reader = csv.reader(f, lineterminator='\n')
        for row in reader:
            raika_tweets.append(row)

    n = int(arg[0]) if arg else 1
    for _ in range(n):
        raika_tweet_pickup = random.choice(raika_tweets)
        for tw in raika_tweet_pickup:
            await ctx.send(tw)


@bot.command()
async def removebg(ctx):
    removebg_apikey = os.getenv('REMOVEBG_APIKEY')

    filename_input = f'data/temp/temp_input_{ctx.channel.id}.png'
    filename_output = f'data/temp/temp_output_{ctx.channel.id}.png'

    if not await modules.funcs.attachments_proc(ctx, filename_input, 'image'):
        return

    async with ctx.typing():
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(filename_input, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': removebg_apikey},
        )

        if response.status_code == requests.codes.ok:
            with open(filename_output, 'wb') as out:
                out.write(response.content)
                await ctx.send(file=discord.File(filename_output))
                for filename in [filename_input, filename_output]:
                    if os.path.isfile(filename):
                        os.remove(filename)
        else:
            await ctx.send(f'```Error:{response.status_code} {response.text}```')


@bot.command(aliases=['grave'])
async def tomb(ctx, *args):
    def contains_emoji(string):
        if re.search(r'<:.+:\d+:>', string):
            result = ['dslfajdlkj', '<:asdfa:234234:>', 'kdlsjf']
            return 
        for chat in string:
            if char in emoji.UNICODE_EMOJI:
                return True
    if args:
        for content in args:
            if len(content) > 279:
                content = content[:279]
            
            if emoji.emoji_count(content) > 0:
                hasemoji = True
            else:
                hasemoji = False
            result = f'{content}のお墓\n\n　　  ＿＿\n　　｜　｜\n'
            content = content.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})).replace(' ', '　')
            for char in content:
                # 
                if hasemoji:
                    if emoji.is_emoji(char):
                        add = f'　　｜{char}｜\n'
                    else:
                        add = f'　　｜ {char} ｜\n'
                else:
                    add = f'　　｜{char}｜\n'
                result += add
            result += '　　｜　｜\n　|￣￣￣￣￣|\n　|　 |三三|　 |'
            await ctx.send(result)


@bot.command()
async def uma(ctx):
    class Chara:
        id = 0
        rarity = 0
        is_pickup = 0

        def __init__(self, id, rarity, is_pickup):
            self.id = id
            self.rarity = rarity
            self.is_pickup = is_pickup

    class Gacha_Usage:
        user = ''
        chara_id_list = []
        exchange_point = 0

        def __init__(self, user, ids, exchange_point):
            self.user = user
            self.chara_id_list = ids
            self.exchange_point = exchange_point
    
    chara_list = []
    usage_list = []
    path_uma_gacha = 'data/assets/uma_gacha'
    path_output = f'data/temp/uma_gacha_{ctx.channel.id}.png'
    fontsize = 32
    region_particle = img_utils.Region([img_utils.Rect(0, 30, 32, 236), img_utils.Rect(32, 30, 207, 56), img_utils.Rect(207, 30, 240, 236)])

    async with ctx.typing():
        with open('data/csv/uma_chara_info.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                chara = Chara(int(row[0]), int(row[1]), int(row[2]))
                chara_list.append(chara)

        with open('data/csv/uma_gacha_usage.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                u = Gacha_Usage(row[0], [int(s) for s in row[1].split('/')], int(row[2]))
                usage_list.append(u)

        chara_id_list = []
        exchange_point = 0
        for i, u in enumerate(usage_list):
            if str(ctx.author) == u.user:
                chara_id_list = u.chara_id_list
                exchange_point = u.exchange_point
                usage_list.pop(i)       

        weights = [79, 18, 3]
        weights_10 = [0, 97, 3]
        
        m_img = modules.img.Mimbot_Image()
        m_img.load(f'{path_uma_gacha}/textures/bg.png')

        for i in range(10):
            w = weights if i < 9 else weights_10

            chara_results_by_rarity = []

            chara_results_by_rarity.append(random.choice([ch for ch in chara_list if ch.rarity == 1]))

            for r in range(2, 4):
                list_pickup = [ch for ch in chara_list if ch.rarity == r and ch.is_pickup]
                list_not_pickup = [ch for ch in chara_list if ch.rarity == r and not ch.is_pickup]
                prob_pickup = 0.75 if r == 3 else 2.25
                if len(list_pickup):
                    chara_results_by_pickup = random.choices(
                        [list_pickup, list_not_pickup],
                        weights=[
                            len(list_pickup) * prob_pickup,
                            w[r - 1] - len(list_pickup) * prob_pickup
                        ]
                        )[0]
                    chara_results_by_rarity.append(random.choice(chara_results_by_pickup))
                else:
                    chara_results_by_rarity.append(random.choice([ch for ch in chara_list if ch.rarity == r]))

            chara_result = random.choices(chara_results_by_rarity, weights=w)[0]

            chara_icon = Image.open(f'{path_uma_gacha}/textures/chara_icon/{chara_result.id}.png')

            x = 0
            y = 0
            if i % 5 < 3:
                x = 96 + 324 * (i % 5)
                y = 157 + 724 * (i // 5)
            else:
                x = 258 + 324 * (i % 5 - 3)
                y = 519 + 724 * (i // 5)

            m_img.composit(chara_icon, (x, y))

            piece_x = 0
            bonus_x = 0
            num_piece = 0
            num_megami = 0
            text_piece_x = 0
            
            if chara_result.rarity == 3:
                num_megami = 20
                if chara_result.is_pickup:
                    num_piece = 90
                else:
                    num_piece = 60
            elif chara_result.rarity == 2:
                num_megami = 3
                num_piece = 10
            else:
                num_megami = 1
                num_piece = 5

            if chara_result.id in chara_id_list:
                adjust_x = -11 if chara_result.rarity == 2 else 0
                megami = Image.open(f'{path_uma_gacha}/textures/icon_megami.png')
                megami_x = 4 if chara_result.rarity == 3 else 26
                m_img.composit(megami, (x + megami_x + adjust_x, y + 300))

                piece_x = 130 + adjust_x
                bonus_x = 134 + adjust_x
                text_piece_x = 182 + adjust_x

                text_megami_x = 54 if chara_result.rarity == 3 else 76
                m_img.drawtext(f'x{num_megami}', (x + text_megami_x + adjust_x, y + 311), fill=(124, 63, 18), anchor='lt', fontpath='.fonts/rodin_wanpaku_eb.otf', fontsize=fontsize, stroke_width=2, stroke_fill='white')

            else:
                chara_id_list.append(chara_result.id)
                label_new = Image.open(f'{path_uma_gacha}/textures/label_new.png')
                m_img.composit(label_new, (x - 22, y))

                adjust_x = 11 if chara_result.rarity == 1 else 0

                piece_x = 65 + adjust_x
                text_piece_x = 117 + adjust_x
                bonus_x = 68 + adjust_x

            m_img.drawtext(f'x{num_piece}', (x + text_piece_x, y + 311), fill=(124, 63, 18), anchor='lt', fontpath='.fonts/rodin_wanpaku_eb.otf', fontsize=fontsize, stroke_width=2, stroke_fill='white')

            piece = Image.open(f'{path_uma_gacha}/textures/piece_icon/{chara_result.id}.png')
            m_img.composit(piece, (x + piece_x, y + 300))

            label_bonus = Image.open(f'{path_uma_gacha}/textures/label_bonus.png')
            m_img.composit(label_bonus, (x + bonus_x, y + 286))

            if chara_result.rarity == 3:
                frame = Image.open(f'{path_uma_gacha}/textures/frame.png')
                m_img.composit(frame, (x - 8, y))

            if chara_result.rarity > 1:
                num_stars = 7 if chara_result.rarity == 3 else 5
                particle = Image.open(f'{path_uma_gacha}/textures/particle_{chara_result.rarity}.png')
                particle_pos = None
                for _ in range(num_stars):
                    scale = random.uniform(1, 3)
                    particle_resize = particle.resize((int(particle.width // scale) ,int(particle.height // scale)))
                    particle_pos = region_particle.randompos()
                    m_img.composit(particle_resize, (x - (particle_resize.width // 2) + particle_pos[0], y - (particle_resize.height // 2) + particle_pos[1]))

            stars = Image.open(f'{path_uma_gacha}/textures/stars_{chara_result.rarity}.png')
            m_img.composit(stars, (x + 46, y + 243))

        m_img.drawtext(str(exchange_point), (732, 1611), fill=(124, 63, 18), anchor='rt', fontpath='.fonts/rodin_wanpaku_eb.otf', fontsize=fontsize)
        exchange_point += 10
        m_img.drawtext(str(exchange_point), (860, 1611), fill=(255, 145, 21), anchor='rt', fontpath='.fonts/rodin_wanpaku_eb.otf', fontsize=fontsize)

        m_img.write(path_output)
        gacha_result_image = discord.File(path_output)
        
        class Button_Uma(discord.ui.Button):
            async def callback(self, interaction):
                response = interaction.response
                await response.edit_message(view=None)
                await uma(ctx)

        button = Button_Uma(style=discord.ButtonStyle.success, label='もう一回引く')

        view = discord.ui.View()
        view.timeout = None
        view.add_item(button)

        await ctx.send(file=gacha_result_image, view=view)

    if os.path.isfile(path_output):
        os.remove(path_output)

    usage = Gacha_Usage(str(ctx.author), chara_id_list, exchange_point)
    usage_list.append(usage)

    with open('data/csv/uma_gacha_usage.csv', 'w') as f:
        writer = csv.writer(f)
        for u in usage_list:
            writer.writerow([u.user, '/'.join([str(n) for n in u.chara_id_list]), u.exchange_point])

            

##########################################################################
####    Run
##########################################################################
token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)
