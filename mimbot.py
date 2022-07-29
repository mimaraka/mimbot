# インストールした discord.py を読み込む
import discord, random, os, csv
from PIL import Image, ImageFont, ImageDraw

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzMwMzczNDE3NjUxNTM1OTMy.GnEN_Z.izW6dcJV39lRsqfY67-LgSxZ9ozXdoTBim-E38'

# 接続に必要なオブジェクトを生成
client = discord.Client()

async def UmaGacha10(message):
    umamusume = [
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
        ["[Maverick]ナリタブライアン", 3],
        ["[サンライト・ブーケ]マヤノトップガン", 3],
        ["[クエルクス・キウィーリス]エアグルーヴ", 3],
        ["[あおぐもサミング]セイウンスカイ", 3],
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
        ["[朔月のマ・シェリ]カレンチャン", 13],
        ["[Titania]ファインモーション", 13]
    ]
    weights = [79, 18, 1.5, 1.5]
    weights_10 = [0, 97, 1.5, 1.5]

    width = 400
    height = 222
    bg = (54, 57, 63)
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(".fonts/meiryo.ttf", 16)
    kankaku = 46

    for i in range(10):
        if (i < 9):
            w = weights
        else:
            w = weights_10
        l_rare = [
            random.choice([i for i in umamusume if i[1] == 1]),
            random.choice([i for i in umamusume if i[1] == 2]),
            random.choice([i for i in umamusume if i[1] == 3]),
            random.choice([i for i in umamusume if i[1] > 10])
        ]
        result = random.choices(l_rare, weights=w)[0]
        if (result[1] % 10 == 3):
            color = (214,204,107)
        else:
            color = (255, 255, 255)
        if (i == 5):
            draw.rectangle((0, 0, width, height), fill=bg)
        #umaim = Image.open(f"C:\\Users\\njotn\\OneDrive\\画像\\umaicon\\resize\\i_{umamusume.index(result)+1}.png")
        #img.paste(umaim, (0, kankaku * (i % 5)))
        draw.text((40,-4 + kankaku * (i % 5)), "★" * (result[1] % 10) + "　" * (3 - result[1] % 10),color,font=font)
        draw.text((40,12 + kankaku * (i % 5)), result[0] ,color,font=font)
        if (i == 4 or i == 9):
            img.save("temp.png")
            await message.channel.send(file=discord.File("temp.png"))
    os.remove("temp.png")
    await message.channel.send(f"author：{message.author}")

    with open('data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([message.author, 2])



# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「!uma」と発言したら10連
    if message.content == '!uma':
        await UmaGacha10(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)