import discord
import os
import rembg
import requests
import modules.funcs
from PIL import Image



REMOVEBG_APIKEY = os.getenv("REMOVEBG_APIKEY")

# 背景を透過
async def proc(itrc, ctx, use_removebgapi=False):
    def rembg_remove(path_i, path_o):
        print("[removebg] Using rembg...")
        image = Image.open(path_i)
        image_output = rembg.remove(image)
        image_output.save(path_o)

    def removebgapi_remove(path_i, path_o):
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": open(path_i, "rb")},
            data={"size": "auto"},
            headers={"X-Api-Key": REMOVEBG_APIKEY},
        )
        if response.status_code == requests.codes.ok:
            print("[removebg] Using removebg API...")
            with open(path_o, "wb") as out:
                out.write(response.content)
        else:
            rembg_remove(path_i, path_o)

    if not itrc and not ctx:
        return

    channel = itrc.channel if itrc else ctx.channel

    filename_input = f"data/temp/temp_input_{channel.id}.png"
    filename_output = f"data/temp/temp_output_{channel.id}.png"

    if itrc:
        await itrc.response.defer()

    if not await modules.funcs.attachments_proc(itrc, ctx, filename_input, "image"):
        return

    if use_removebgapi:
        removebgapi_remove(filename_input, filename_output)
    else:
        rembg_remove(filename_input, filename_output)
    if itrc:
        await itrc.followup.send(file=discord.File(filename_output))
    elif ctx:
        await ctx.send(file=discord.File(filename_output))

    for filename in [filename_input, filename_output]:
        if os.path.isfile(filename):
            os.remove(filename)