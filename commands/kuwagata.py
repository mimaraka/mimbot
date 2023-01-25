# クワガタ
async def proc(itrc, ctx, kuwagata_text="クワガタ"):
    if not itrc and not ctx:
        return
    user = itrc.user if itrc else ctx.author
    result = f"{user.display_name}さん見て見て\n{kuwagata_text}～"

    if itrc:
        await itrc.response.send_message(result)
    elif ctx:
        await ctx.send(result)