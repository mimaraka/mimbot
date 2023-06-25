import discord

# 任意のメッセージを送信
async def proc(itrc, ctx, bot, content, channel_id=None):
    if not itrc and not ctx:
        return
    
    error_mes = ""

    try:
        this_channel = itrc.channel if itrc else ctx.channel
        channel = await bot.fetch_channel(int(channel_id)) if channel_id else this_channel
        await channel.send(content[:2000])
    except ValueError:
        error_mes = "チャンネルIDが無効です。"
    except discord.NotFound:
        error_mes = "指定したチャンネルIDが存在しません。"
    except discord.Forbidden:
        error_mes = "指定したチャンネルでメッセージを送信する権限がありません。"
    except (discord.InvalidData, discord.HTTPException):
        error_mes = "メッセージの送信に失敗しました。"

    if error_mes:
        embed = discord.Embed(title="エラー", description=error_mes)
        if itrc:
            await itrc.response.send_message(embed=embed)
        else:
            await ctx.send(embed=embed)
        return
    
    if itrc:
        embed = discord.Embed(description="メッセージを送信しました。")
        await itrc.response.send_message(embed=embed)