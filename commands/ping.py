# Ping
async def proc(itrc, ctx, bot):
    # Ping値を秒単位で取得
    raw_ping = bot.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000, 2)
    result = f"Pong! `Latency: {ping}[ms]`"
    if itrc:
        await itrc.response.send_message(result)
    elif ctx:
        await ctx.send(result)