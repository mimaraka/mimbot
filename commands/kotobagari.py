import csv



# 言葉狩り機能のオンオフ
async def proc(itrc, ctx, mode):
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