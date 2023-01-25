# おくり
async def proc(itrc, ctx, seiyoku="性欲", aru="ある", no="の"):
    text = f"おくりさんどれだけ{seiyoku}{aru}{no}"

    if itrc:
        await itrc.response.send_message(text)
    elif ctx:
        await ctx.send(text)