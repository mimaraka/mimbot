# カニ
async def proc(itrc, ctx, kani_text="カニ"):
    if not itrc and not ctx:
        return
    user = itrc.user if itrc else ctx.author
    result = f"見て見て{user.display_name}さん\n{kani_text}ファル子だよ～"

    if itrc:
        await itrc.response.send_message(result)
    elif ctx:
        await ctx.send(result)