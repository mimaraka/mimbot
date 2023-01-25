import discord
import modules.img
import os



# クワガタ(画像)
async def proc(itrc, ctx, kuwagata_text="クワガタ"):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel
    user = itrc.user if itrc else ctx.author

    async with channel.typing():
        filename_output = f"data/temp/temp_output_{channel.id}.png"
        m_img = modules.img.Mimbot_Image()
        m_img.load("data/assets/kuwagata_base.png")
        # 〇〇さん
        m_img.drawtext(
            f"{user.display_name}さん",
            (579, 22),
            fill="black",
            anchor="rt",
            fontsize=24,
            direction="ttb"
        )
        # 〇〇～
        str_kuwagata = f"{kuwagata_text}～"
        lines = []
        line = ""
        for i, char in enumerate(str_kuwagata):
            if i % 29 == 0 and i != 0:
                lines.append(line)
                line = ""
            line += char
            if i == len(str_kuwagata) - 1:
                lines.append(line)
        for i, l in enumerate(lines):
            m_img.drawtext(
                l,
                (283 - i * 32, 18),
                fill="black",
                anchor="rt",
                fontsize=28,
                direction="ttb"
            )

        if not m_img.image is None:
            m_img.image.save(filename_output)
        if itrc:
            await itrc.response.send_message(file=discord.File(filename_output))
        elif ctx:
            await ctx.send(file=discord.File(filename_output))
        if os.path.isfile(filename_output):
            os.remove(filename_output)