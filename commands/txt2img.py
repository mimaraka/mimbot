import discord
import stable_diffusion.scripts.txt2img
import os
import glob



g_models = None

#Text to image(Stable Diffusion)
async def proc(itrc, ctx):
    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

    filename_output = f"anythingv3_t2i_o_{channel.id}"
    output_dir = f"data/temp"
    result_path = f"{output_dir}/{filename_output}.png"
    def_ckpt = ""
    MODEL_DIR = "stable_diffusion/models"
    DEF_N_STEPS = 24
    DEF_WIDTH = 512
    DEF_HEIGHT = 512

    class Modal_SdSettings(discord.ui.Modal):
        def __init__(self):
            super().__init__(title="Stable Diffusionの設定", timeout=None)
            # プロンプト
            self.input_prompt = discord.ui.TextInput(
                label="プロンプト",
                required=True,
                style=discord.TextStyle.paragraph
            )

                # ネガティブプロンプト
            self.input_negative_prompt = discord.ui.TextInput(
                label="ネガティブプロンプト",
                required=False,
                style=discord.TextStyle.paragraph
            )

            # サンプリングのステップ数
            self.input_sampling_steps = discord.ui.TextInput(
                label="サンプリングのステップ数",
                style=discord.TextStyle.short,
                default=f"{DEF_N_STEPS}"
            )

            # 画像の幅
            self.input_width = discord.ui.TextInput(
                label="画像の幅",
                style=discord.TextStyle.short,
                default=f"{DEF_WIDTH}"
            )

            # 画像の高さ
            self.input_height = discord.ui.TextInput(
                label="画像の高さ",
                style=discord.TextStyle.short,
                default=f"{DEF_HEIGHT}"
            )

            self.add_item(self.input_prompt)
            self.add_item(self.input_negative_prompt)
            self.add_item(self.input_sampling_steps)
            self.add_item(self.input_width)
            self.add_item(self.input_height)

        async def on_submit(self, interaction):
            global g_models
            try:
                prompt = str(self.input_prompt)
                neg_prompt = str(self.input_negative_prompt)
                n_step = int(str(self.input_sampling_steps))
                width = int(str(self.input_width))
                height = int(str(self.input_height))

            except ValueError:
                await interaction.channel.send(
                    embed=discord.Embed(
                        title="エラー",
                        description="無効な入力値です。"
                    )
                )

            # インタラクションを無視
            try:
                await interaction.response.send_message("")
            except discord.errors.HTTPException:
                pass

            message = None

            if (not g_models) or (not button_continue.ckpt_ in g_models.keys()):
                message = await channel.send(
                    embed=discord.Embed(
                        title="処理中です...",
                        description="モデルの読み込み中..."
                    )
                )
                g_models = stable_diffusion.scripts.txt2img.load_model(button_continue.ckpt_, models=g_models)

            embed_creating = discord.Embed(
                title="処理中です...",
                description="生成中..."
            )

            if message:
                await message.edit(embed=embed_creating)
            else:
                message = await channel.send(embed=embed_creating)

            stable_diffusion.scripts.txt2img.txt2img_proc(
                prompt=prompt,
                negative_prompt=neg_prompt,
                filename=filename_output,
                outdir=output_dir,
                ckpt=button_continue.ckpt_,
                sampling_method=button_continue.sampling_method_,
                sampling_steps=n_step,
                width=width,
                height=height,
                models=g_models
            )
            await message.delete()

            if os.path.isfile(result_path):
                if itrc:
                    await itrc.followup.send(file=discord.File(result_path))
                elif ctx:
                    await ctx.send(file=discord.File(result_path))
                os.remove(result_path)

    if itrc:
        await itrc.response.defer()

    modal_settings = Modal_SdSettings()

    # モデルを指定するコンボボックス
    class My_Select(discord.ui.Select):
        async def callback(self, interaction):
            # インタラクションを無視
            try:
                await interaction.response.send_message("")
            except discord.errors.HTTPException:
                pass

    # "続ける"のボタン
    class Button_Continue(discord.ui.Button):
        ckpt_ = ""
        sampling_method_ = ""
        async def callback(self, interaction):
            await interaction.message.delete()
            await interaction.response.send_modal(modal_settings)
            if not list_models.values:
                self.ckpt_ = def_ckpt
            else:
                self.ckpt_ = list_models.values[0]

            if not list_sampling_methods.values:
                self.sampling_method_ = "ddim"
            else:
                self.sampling_method_ = list_sampling_methods.values[0]


    list_models = My_Select(min_values=1, max_values=1)
    models = [os.path.split(model)[1] for model in glob.glob(f"{MODEL_DIR}/*.ckpt")]
    if not models:
        await channel.send(
                    embed=discord.Embed(
                        title="エラー",
                        description="モデル(.ckpt)が見つかりません。"
                    )
                )
        return
    def_ckpt = models[0]
    for i, model in enumerate(models):
        list_models.add_option(label=model, value=model, default=i==0)

    
    list_sampling_methods = My_Select(min_values=1, max_values=1)
    list_sampling_methods.add_option(label="DDIM", value="ddim", default=True)
    list_sampling_methods.add_option(label="DPM solver", value="dpm_solver")
    list_sampling_methods.add_option(label="PLMS", value="plms")

    button_continue = Button_Continue(label="続ける")

    view = discord.ui.View()
    view.timeout = None
    view.add_item(list_models)
    view.add_item(list_sampling_methods)
    view.add_item(button_continue)

    await channel.send(
        embed=discord.Embed(title="モデル・サンプリング方法を選択："),
        view=view
    )