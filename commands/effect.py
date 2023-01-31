import discord
import modules.img
import modules.funcs
import os



# 画像に各種エフェクトをかける
async def proc(itrc, ctx):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

    # コンボボックス
    class My_Select(discord.ui.Select):
        async def callback(self, interaction):
            # インタラクションを無視
            try:
                await interaction.response.send_message("")
            except discord.errors.HTTPException:
                pass

    # "続ける"のボタン
    class Button_Continue(discord.ui.Button):
        async def callback(self, interaction):
            return

    if not await modules.funcs.attachments_proc(itrc, ctx, filename_input, "image"):
        return

    # 画像読み込み
    m_img = modules.img.Mimbot_Image()
    m_img.load(filename_input)
    
    list_effects = My_Select(min_values=1, max_values=1)

    list_effects.add_option(label="ブラー", value="blur")
    list_effects.add_option(label="エンボス", value="emboss")
    list_effects.add_option(label="ディストーション", value="distortion")
    list_effects.add_option(label="モザイク", value="mosaic")
    list_effects.add_option(label="ネガポジ反転", value="negative")
    list_effects.add_option(label="ドット化", value="pixelize")

    embed = discord.Embed(
        title = "effect command",
        description = 
            "**・ブラー**\n画像にブラーを適用します。\n\n"\
            "**・エンボス**\n画像にエンボスを適用します。\n\n"\
            "**・ディストーション**\n画像を様々な形に変形します。\n\n"\
            "**・モザイク**\n画像にモザイクを適用します。\n\n"\
            "**・ネガポジ反転**\n画像のネガポジを反転します。\n\n"\
            "**・ドット化**\n画像をドット絵風の見た目にします。"
    )

    button_continue = Button_Continue(label="続ける")

    view = discord.ui.View()
    view.timeout = None
    view.add_item(list_effects)
    view.add_item(button_continue)

    await channel.send(
        embed=embed,
        view=view
    )


    async with channel.typing():
        filename_input = f"data/temp/temp_input_{channel.id}.png"
        filename_output = f"data/temp/temp_output_{channel.id}.png"

        if not await modules.funcs.attachments_proc(itrc, ctx, filename_input, "image"):
            return

        m_img = modules.img.Mimbot_Image()
        m_img.load(filename_input)

        # ブラー
        async def blur():
            class Button_Continue_Blur(discord.ui.Button):
                async def callback(self, interaction):
                    
                    return
            
            list_blur = My_Select(min_values=1, max_values=1)
            list_blur.add_option(label="ボックス", value="box")
            list_blur.add_option(label="ガウシアン", value="gaussian")
            list_blur.add_option(label="メディアン", value="median")
            list_blur.add_option(label="最大値", value="max")
            list_blur.add_option(label="最小値", value="min")
            list_blur.add_option(label="ランク", value="rank")

            button_continue_blur = Button_Continue_Blur(label="続ける")
            
            embed = discord.Embed(
                title = "ブラー",
                description = 
                    "**・ボックス (サイズ)**\nボックスブラー\n\n"\
                    "**・ガウシアン (サイズ)**\nガウシアンブラー\n\n"\
                    "**・メディアン (サイズ)**\nメディアンブラー\n\n"\
                    "**・最大値 (サイズ)**\n最大値フィルタ\n\n"\
                    "**・最小値 (サイズ)**\n最小値フィルタ\n\n"\
                    "**・ランク (サイズ) (ランク)**\nランクフィルタ"
            )

            view = discord.ui.View()
            view.timeout = None
            view.add_item(list_blur)
            view.add_item(button_continue_blur)

            await channel.send(embed=embed, view=view)

        # 変形
        async def distortion():
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
        async def emboss():
            m_img.emboss()

        # モザイク
        async def mosaic():
            size = int(values[0]) if values else 20
            m_img.mosaic(size)

        # ネガポジ反転
        async def negative():
            m_img.negative()

        # Pixelize
        async def pixelize():
            size = int(values[0]) if values else 20
            m_img.pixelize(size)

        if not m_img.image is None:
            #cv2.imwrite("temp_output.png",img_result)
            m_img.image.save(filename_output)

        await channel.send(file=discord.File(filename_output))

        for filename in [filename_input, filename_output]:
            if os.path.isfile(filename):
                os.remove(filename)