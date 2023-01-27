import discord
import modules.img
import os



# カニ(画像)
async def proc(itrc, ctx, kani_text="カニ"):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel
    user = itrc.user if itrc else ctx.author

    async with channel.typing():
        filename_output = f"data/temp/temp_output_{channel.id}.png"
        m_img = modules.img.Mimbot_Image()
        m_img.load("data/assets/kani_bg.png")
        # 〇〇さん
        m_img.drawtext(
            f"{user.display_name}さん",
            (529, 15),
            fill="black",
            anchor="rt",
            fontsize=27,
            direction="ttb"
        )
        # 〇〇ファル子だよ～
        str_kani = f"{kani_text}ファル子"
        str_suffix = "だよ～"
        lines = []
        line = ""
        for i, char in enumerate(str_kani):
            # 29文字で改行
            if i % 29 == 0 and i != 0:
                lines.append(line)
                line = ""
            line += char
            if i == len(str_kani) - 1:
                lines.append(line)

        # '〇〇ファル子'の部分が2行以上のとき
        if len(lines) > 1:
            # 最後の行の文字数が27文字以上のとき
            if len(lines[-1]) > 26:
                lines[-1] += str_suffix[:29 - len(lines[-1])]
                lines.append(str_suffix[29 - len(lines[-1]):])
            else:
                lines[-1] += str_suffix
        else:
            lines.append(str_suffix)

        for i, l in enumerate(lines):
            m_img.drawtext(
                l,
                (291 - i * 41, 19),
                fill="black",
                anchor="rt",
                fontsize=27,
                direction="ttb"
            )

        # 〇〇...ですね...
        m_img.drawtext(
            f"{kani_text}…ですね…",
            (68, 42),
            fill="black",
            anchor="rt",
            fontsize=36,
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