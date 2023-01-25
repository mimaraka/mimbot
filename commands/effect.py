import discord
import modules.img
import modules.funcs
import os



# 画像に各種エフェクトをかける
async def proc(itrc, ctx, prompt=""):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

    args = prompt.split(",")

    if args:
        fxname = args[0]
    else:
        embed = discord.Embed(
            title = "effect command",
            description = 
                "**・blur (ブラーの種類)**\n画像にブラーを適用します。\n\n"\
                "**・distortion / distort / dist (変形の種類)：**\n画像を様々な形に変形します。\n\n"\
                "**・mosaic (サイズ)：**\n画像にモザイクを適用します。\n\n"\
                "**・negative / nega：**\n画像のネガポジを反転します。\n\n"\
                "**・pixelize (サイズ)：**\n画像をドット絵風の見た目にします。"
        )
        if itrc:
            await itrc.response.send_message(embed=embed)
        elif ctx:
            await ctx.send(embed=embed)
        return

    if len(args) > 1:
        values = args[1:]
    else:
        values = []

    async with channel.typing():
        filename_input = f"data/temp/temp_input_{channel.id}.png"
        filename_output = f"data/temp/temp_output_{channel.id}.png"

        if not await modules.funcs.attachments_proc(itrc, ctx, filename_input, "image"):
            return

        m_img = modules.img.Mimbot_Image()
        m_img.load(filename_input)

        # ブラー
        if fxname.lower() in ["blur", "bl"]:
            if m_img.blur(values):
                embed = discord.Embed(
                    title = "blur effect",
                    description = 
                        "**・box (サイズ)：**\nボックスブラー\n\n"\
                        "**・gaussian (サイズ)：**\nガウシアンブラー\n\n"\
                        "**・median (サイズ)：**\nメディアンブラー\n\n"\
                        "**・maximun / max (サイズ)：**\n最大値フィルタ\n\n"\
                        "**・minimum / min (サイズ)：**\n最小値フィルタ\n\n"\
                        "**・rank (サイズ) (ランク)：**\nランクフィルタ"
                )
                await channel.send(embed = embed)
                return

        # 変形
        elif fxname.lower() in ["dist", "distort", "distortion"]:
            if m_img.distort(values):
                embed = discord.Embed(
                    title = "distort effect",
                    description = 
                        "**・vortex (適用量)：**\n渦ワープ\n\n"\
                        "**・wave / wav (振幅) (周期)：**\n波形ワープ"
                )
                await channel.send(embed = embed)
                return

        # エンボス
        elif fxname.lower() == "emboss":
            m_img.emboss()

        # モザイク
        elif fxname.lower() == "mosaic":
            size = int(values[0]) if values else 20
            m_img.mosaic(size)

        # ネガポジ反転
        elif fxname in ["negative", "nega"]:
            m_img.negative()

        # Pixelize
        elif fxname.lower() == "pixelize":
            size = int(values[0]) if values else 20
            m_img.pixelize(size)

        if not m_img.image is None:
            #cv2.imwrite("temp_output.png",img_result)
            m_img.image.save(filename_output)

        await channel.send(file=discord.File(filename_output))

        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)