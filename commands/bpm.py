# async def bpm(itrc):
#     duration = 30
#     x_sr = 200
#     bpm_min, bpm_max = 60, 240

#     if itrc.message.reference is None:
#         await itrc.reply("適用したい音声ファイルが添付されたメッセージに返信してください", mention_author=False)
#         return

#     mes = await itrc.channel.fetch_message(itrc.message.reference.message_id)

#     if mes.attachments[0] is None:
#         await itrc.reply("返信元のメッセージにファイルが添付されていません", mention_author=False)
#         return

#     file_name = mes.attachments[0].filename

#     await mes.attachments[0].save(file_name)

#     mes_pros = await itrc.reply("処理中です…", mention_author=False)

#     # 楽曲の信号を読み込む
#     y, sr = librosa.load(file_name, offset=38, duration=duration, mono=True)

#     # ビート検出用信号の生成
#     # リサンプリング & パワー信号の抽出
#     x = np.abs(librosa.resample(y, sr, x_sr)) ** 2
#     x_len = len(x)

#     # 各BPMに対応する複素正弦波行列を生成
#     M = np.zeros((bpm_max, x_len), dtype=np.complex)
#     for bpm in range(bpm_min, bpm_max): 
#         thete = 2 * np.pi * (bpm/60) * (np.arange(0, x_len) / x_sr)
#         M[bpm] = np.exp(-1j * thete)

#     # 各BPMとのマッチング度合い計算
#     #（複素正弦波行列とビート検出用信号との内積）
#     x_bpm = np.abs(np.dot(M, x))

#     # BPM値を算出
#     bpm = np.argmax(x_bpm)

#     await mes_pros.delete()
#     await itrc.channel.send(f"BPM: {bpm}")
#     os.remove(file_name)