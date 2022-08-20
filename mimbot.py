from discord.ext import commands
#import cv2
#herokuでcv2をimportするとエラーが出たのでとりあえずPillowで代用
import discord
import glob
from PIL import Image, ImageFont, ImageDraw
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
####    Functions
##########################################################################

#添付ファイル処理用の関数
async def attachments_procedure(ctx):
    #返信をしていなかった場合
    if ctx.message.reference is None:
        #直前のメッセージの添付ファイルの取得を試みる
        
        await ctx.reply('ファイルが添付されたメッセージに返信してください', mention_author=False)
        return

    mes = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    if mes.attachments[0] is None:
        await ctx.reply('返信元のメッセージにファイルが添付されていません', mention_author=False)
        return



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

    if re.search(r"(お|オ|o)((\s*|᠎*)*|.{,3})(く|ク|ku)((\s*|᠎*)*|.{,3})(り|リ|ri)", str(ctx.content)):
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


@bot.command()
async def debug(ctx):
    messages = [message async for message in ctx.channel.history(limit=10)]
    for i in range(10):
        await ctx.send(messages[i].content)


# ウマ娘ガチャシミュレーター
@bot.command()
async def uma(ctx):
    uma_gacha_lists = [
        # [ウマ娘の名称, レア度(ピックアップは+10)]
        # ガチャ詳細サイト
        # https://umamusume.cygames.jp/#/gacha
        ["[スペシャルドリーマー]スペシャルウィーク", 3],
        ["[サイレントイノセンス]サイレンススズカ", 3],
        ["[トップ・オブ・ジョイフル]トウカイテイオー", 3],
        ["[フォーミュラオブルージュ]マルゼンスキー", 3],
        ["[スターライトビート]オグリキャップ", 3],
        ["[ワイルド・フロンティア]タイキシャトル", 3],
        ["[エレガンス・ライン]メジロマックイーン", 3],
        ["[ロード・オブ・エンペラー]シンボリルドルフ", 3],
        ["[ローゼスドリーム]ライスシャワー", 3],
        ["[レッドストライフ]ゴールドシップ", 2],
        ["[ワイルドトップギア]ウオッカ", 2],
        ["[トップ・オブ・ブルー]ダイワスカーレット", 2],
        ["[石穿つ者]グラスワンダー", 2],
        ["[エル☆Número１]エルコンドルパサー", 2],
        ["[エンプレスロード]エアグルーヴ", 2],
        ["[すくらんぶる☆ゾーン]マヤノトップガン", 2],
        ["[マーマリングストリーム]スーパークリーク", 2],
        ["[ストレート・ライン]メジロライアン", 1],
        ["[tach-nology]アグネスタキオン", 1],
        ["[Go To Winning]ウイニングチケット", 1],
        ["[サクラ、すすめ！]サクラバクシンオー", 1],
        ["[うららん一等賞♪]ハルウララ", 1],
        ["[運気上昇☆幸福万来]マチカネフクキタル", 1],
        ["[ポインセチア・リボン]ナイスネイチャ", 1],
        ["[キング・オブ・エメラルド]キングヘイロー", 1],
        ["[オー・ソレ・スーオ！]テイエムオペラオー", 3],
        ["[MB-19890425]ミホノブルボン", 3],
        ["[pf.Victory formula...]ビワハヤヒデ", 3],
        ["[ビヨンド・ザ・ホライズン]トウカイテイオー", 3],
        ["[エンド・オブ・スカイ]メジロマックイーン", 3],
        ["[フィーユ・エクレール]カレンチャン", 3],
        ["[Nevertheless]ナリタタイシン", 3],
        ["[あぶそりゅーと☆LOVE]スマートファルコン", 3],
        ["[Maverick]ナリタブライアン", 13],
        ["[サンライト・ブーケ]マヤノトップガン", 3],
        ["[クエルクス・キウィーリス]エアグルーヴ", 3],
        ["[あおぐもサミング]セイウンスカイ", 13],
        ["[アマゾネス・ラピス]ヒシアマゾン", 3],
        ["[ククルカン・モンク]エルコンドルパサー", 3],
        ["[セイントジェード・ヒーラー]グラスワンダー", 3],
        ["[シューティングスタァ・ルヴュ]フジキセキ", 3],
        ["[オーセンティック/1928]ゴールドシチー", 3],
        ["[ほっぴん♪ビタミンハート]スペシャルウィーク", 3],
        ["[ぶっとび☆さまーナイト]マルゼンスキー", 3],
        ["[ブルー/レイジング]メイショウドトウ", 3],
        ["[Meisterscaft]エイシンフラッシュ", 3],
        ["[吉兆・初あらし]マチカネフクキタル", 3],
        ["[ボーノ☆アラモーダ]ヒシアケボノ", 3],
        ["[超特急！フルカラー特殊PP]アグネスデジタル", 3],
        ["[Make up Vampire!]ライスシャワー", 3],
        ["[シフォンリボンマミー]スーパークリーク", 3],
        ["[プリンセス・オブ・ピンク]カワカミプリンセス", 3],
        ["[Creeping Black]マンハッタンカフェ", 3],
        ["[皓月の弓取り]シンボリルドルフ", 3],
        ["[秋桜ダンツァトリーチェ]ゴールドシチー", 3],
        ["[ポップス☆ジョーカー]トーセンジョーダン", 3],
        ["[ツイステッド・ライン]メジロドーベル", 3],
        ["[キセキの白星]オグリキャップ", 3],
        ["[ノエルージュ・キャロル]ビワハヤヒデ", 3],
        ["[Noble Seamair]ファインモーション", 3],
        ["[疾風迅雷]タマモクロス", 3],
        ["[初うらら♪さくさくら]ハルウララ", 3],
        ["[初晴・青き絢爛]テイエムオペラオー", 3],
        ["[日下開山・花あかり]サクラチヨノオー", 3],
        ["[CODE：グラサージュ]ミホノブルボン", 3],
        ["[コレクト・ショコラティエ]エイシンフラッシュ", 3],
        ["[クリノクロア・ライン]メジロアルダン", 3],
        ["[Starry Nocturne]アドマイヤベガ", 3],
        ["[錦上・大判御輿]キタサンブラック", 3],
        ["[ぱんぱかティルトット]マチカネタンホイザ", 2],
        ["[Natural Brilliance]サトノダイヤモンド", 3],
        ["[ブリュニサージュ・ライン]メジロブライト", 3],
        ["[ソワレ・ド・シャトン]セイウンスカイ", 3],
        ["[シュクセ・エトワーレ]フジキセキ", 3],
        ["[ティアード・ペタル]ニシノフラワー", 3],
        ["[四白流星の襲]ヤエノムテキ", 3],
        ["[RUN&WIN]ナイスネイチャ", 3],
        ["[白く気高き激励の装]キングヘイロー", 3],
        ["[オールタイム・フィーバー]アイネスフウジン", 3],
        ["[Like Breakthrough]メジロパーマー", 3],
        ["[朔月のマ・シェリ]カレンチャン", 3],
        ["[Titania]ファインモーション", 3],
        ["[稲荷所縁江戸紫]イナリワン", 3],
        ["[プラタナス・ウィッチ]スイープトウショウ", 3],
        ["[Bubblegum☆Memories]タイキシャトル", 3],
        ["[バカンス・サフィール]メジロドーベル", 3],
        ["[unsigned]エアシャカール", 3]
    ]

    # 確率比[★1, ★2, ★3, ピックアップ]
    weights = [79, 18, 1.5, 1.5]
    # 確率比(10回目)
    weights_10 = [0, 97, 1.5, 1.5]

    # 画像サイズ
    width = 400
    height = 222
    # 項目の間隔
    margin = 45
    # 画像の背景色
    bg = (54, 57, 63)
    # 画像の初期化
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(".fonts/meiryo.ttf", 16)

    for i in range(10):
        w = weights if i < 9 else weights_10

        # レア度ごとに選出
        uma_gacha_results_by_rarity = [
            random.choice(list(filter(lambda e: e[1] == 1, uma_gacha_lists))),
            random.choice(list(filter(lambda e: e[1] == 2, uma_gacha_lists))),
            random.choice(list(filter(lambda e: e[1] == 3, uma_gacha_lists))),
            random.choice(list(filter(lambda e: e[1] > 10, uma_gacha_lists)))
        ]

        # 最終的な排出ウマ娘を決定
        uma_gacha_result = random.choices(uma_gacha_results_by_rarity, weights=w)[0]

        # レア度が3なら文字色を変える
        color = (214, 204, 107) if uma_gacha_result[1] % 10 == 3 else (255, 255, 255)

        # 原寸で表示される最大の画像サイズが400x300(10連だと見切れる)なので5連ずつ2枚の画像に分ける
        if i % 5 == 0:
            draw.rectangle((0, 0, width, height), fill=bg)

        # アイコン画像をuma_iconフォルダから読み込み&貼り付け(URLから読み込むと遅かった)
        uma_image = Image.open(f"resources/uma_icon/i_{uma_gacha_lists.index(uma_gacha_result) + 1}.png")
        img.paste(uma_image, (3, margin * (i % 5) + 5))

        # テキストを描画(星マーク)
        draw.text((40, margin * (i % 5)), "★" * (uma_gacha_result[1] % 10), color, font=font)
        # テキストを描画(ウマ娘名称)
        draw.text((40, margin * (i % 5) + 15), uma_gacha_result[0], color, font=font)

        # 5連ごとに画像を書き出し
        if i % 5 == 4:
            img.save(f"resources/temporally/uma_gacha_{ctx.channel.id}_{int(i / 5) + 1}.png")

    glob_uma_gacha_result_images = glob.glob(f"resources/temporally/uma_gacha_{ctx.channel.id}_*.png")

    uma_gacha_result_images = list(map(lambda e: discord.File(e), glob_uma_gacha_result_images))
    await ctx.channel.send(files=uma_gacha_result_images)

    for file in glob_uma_gacha_result_images:
        if os.path.isfile(file):
            os.remove(file)



##########################################################################
####    Run
##########################################################################

# Botの起動とDiscordサーバーへの接続
token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)