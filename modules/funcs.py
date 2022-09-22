import aiohttp
import csv
import random
import re
import requests


async def attachments_proc(ctx, filepath, media_type):
    async def ismimetype(url, mimetypes_list):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        mime = resp.headers.get('Content-type', '').lower()
                        if any([mime == x for x in mimetypes_list]):
                            return True
                        else:
                            return False
        except:
            return False

    mimetypes = {
        'image':            ['image/png', 'image/pjpeg', 'image/jpeg', 'image/x-icon'],
        'animation_gif':    ['image/gif'],
        'audio':            ['audio/wav', 'audio/mpeg', 'audio/aac', 'audio/ogg'],
        'video':            ['video/mpeg', 'video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo']
    }
    
    url = ''
    if ctx.message.reference is not None:
        message_reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(message_reference.attachments) > 0:
            url = message_reference.attachments[0].url
        else:
            await ctx.reply('返信元のメッセージにファイルが添付されていません', mention_author=False)
            return False
    else:
        async for message in ctx.history(limit=10):
            mo = re.search(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', message.content)
            if len(message.attachments) > 0:
                url = message.attachments[0].url
            elif mo:
                url = mo.group()
            if await ismimetype(url, mimetypes[media_type]):
                break
        else:
            await ctx.reply('ファイルやurlが添付されたメッセージの近くに書くか、返信をしてください', mention_author=False)
            return False

    response = requests.get(url)
    image = response.content
    with open(filepath, "wb") as f:
        f.write(image)
        return True


def searchex(lis, target_text, strength):
    pattern = r''
    for i, el in enumerate(lis):
        if type(el) == list:
            rchar = r''
            for j, s in enumerate(el):
                if j == len(el) - 1:
                    rchar += r'{}'.format(s)
                else:
                    rchar += r'{}'.format(s) + r'|'
            if i == len(lis) - 1:
                pattern += r'(' + rchar + r')'
            else:
                pattern += r'(' + rchar + r')' + r'((\s*|᠎*)*|.{,' + r'{}'.format(strength) + r'})'
        elif type(el) == str:
            rstr = r''
            for j, c in enumerate(el):
                if j == len(el) - 1:
                    rstr += r'{}'.format(c)
                else:
                    rstr += r'{}'.format(c) + r'((\s*|᠎*)*|.{,' + r'{}'.format(strength) + r'})'
            if i == len(lis) - 1:
                pattern += r'(' + rstr + r')'
            else:
                pattern += r'(' + rstr + r')' + r'|'
        else:
            return False
    if re.search(pattern, target_text):
        return True
    else:
        return False


async def kotobagari_proc(ctx):
    if ctx.author.bot:
        return

    channel_id_list = []
    with open('data/csv/kotobagari.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                channel_id_list = row
    
    if not str(ctx.channel.id) in channel_id_list:
        if searchex(['あつい', 'アツい', '暑'], str(ctx.content), 1):
            await ctx.channel.send('https://cdn.discordapp.com/attachments/1002875196522381325/1003853181777887282/temp_output.png')

        if searchex([['お', 'オ'], ['く', 'ク'], ['り', 'リ']], str(ctx.content), 3):
            await ctx.channel.send('おくりさんどれだけ性欲あるの')

        if searchex([['ご', 'ゴ'], ['き', 'キ'], ['ぶ', 'ブ'], ['り', 'リ']], str(ctx.content), 1):
            await ctx.channel.send('フラッシュさん見て見て\nゴキブリ～')

        if searchex(['さかな', 'サカナ', '魚'], str(ctx.content), 1):
            await ctx.channel.send('https://cdn.discordapp.com/attachments/1002875196522381325/1010464389352148992/lycoris4bd_Trim_AdobeExpress.gif')

        if searchex(['ひる', 'ヒル', '昼'], str(ctx.content), 1):
            images = [
                'https://cdn.discordapp.com/attachments/1002875196522381325/1003699645458944011/FTakxQUaIAAoyn3CUnetnoise_scaleLevel2x4.000000.png',
                'https://cdn.discordapp.com/attachments/1002875196522381325/1008245051077443664/FZmJ06EUIAAcZNi.jpg'
            ]
            image_pickup = random.choice(images)
            await ctx.channel.send(image_pickup)
