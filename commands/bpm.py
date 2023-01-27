import librosa
import numpy as np
import discord
import os
import modules.funcs



async def proc(itrc, ctx):
    DURATION = 30
    X_SR = 200
    BPM_MIN, BPM_MAX = 60, 240

    if not itrc and not ctx:
        return
    channel = itrc.channel if itrc else ctx.channel

    async with channel.typing():
        filename_input = f"data/temp/bpm_input_{channel.id}.mp3"

        if not await modules.funcs.attachments_proc(itrc, ctx, filename_input, "audio"):
            return

        # 楽曲の信号を読み込む
        y, sr = librosa.load(filename_input, offset=38, duration=DURATION, mono=True)

        # ビート検出用信号の生成
        # リサンプリング & パワー信号の抽出
        x = np.abs(librosa.resample(y, orig_sr=sr, target_sr=X_SR)) ** 2
        x_len = len(x)

        # 各BPMに対応する複素正弦波行列を生成
        M = np.zeros((BPM_MAX, x_len), dtype=np.complex)
        for bpm in range(BPM_MIN, BPM_MAX):
            thete = 2 * np.pi * (bpm/60) * (np.arange(0, x_len) / X_SR)
            M[bpm] = np.exp(-1j * thete)

        # 各BPMとのマッチング度合い計算
        #（複素正弦波行列とビート検出用信号との内積）
        x_bpm = np.abs(np.dot(M, x))

        # BPM値を算出
        bpm = np.argmax(x_bpm)

        result = discord.Embed(title="BPM", description=str(bpm))

        if itrc:
            await itrc.response.send_message(embed=result)
        elif ctx:
            await channel.send(embed=result)

        if os.path.isfile(filename_input):
            os.remove(filename_input)