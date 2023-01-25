import emoji
import re



# 墓
async def proc(itrc, ctx, content=""):
    def contains_emoji(string):
        # オリジナルの絵文字を含む場合
        if re.search(r"<:.+:\d+:>", string):

            result = ["", "", ""]
            return 
        # デフォルトの絵文字を含む場合
        for char in string:
            if char in emoji.UNICODE_EMOJI:
                return True

    def create_tomb(cont = ""):
        content_ = cont.replace("\n", "")

        has_emoji = False
        tomb_top = "　　   ＿＿"
        tomb_left = ""
        tomb_right = "｜"
        tomb_bottom = "　|￣￣￣￣￣|\n　|　 |三三|　 |"
        tomb_blank = ""

        if emoji.emoji_count(content_) > 0:
            has_emoji = True
            tomb_left = "　　｜"
            tomb_blank = " 　 "
        else:
            has_emoji = False
            tomb_left = "　　 ｜"
            tomb_blank = "　"
            
        while True:
            result = f"{content_}{'の' if cont else ''}お墓\n\n{tomb_top}\n{tomb_left}{tomb_blank}{tomb_right}\n"
            # 半角英数字記号スペースを全角に変換
            # 伸ばし棒(ー)も縦に変換
            content_tmp = content_.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})).replace(" ", "　").replace("ー", "｜") if cont else "　"
            for char in content_tmp:
                if has_emoji:
                    if emoji.is_emoji(char):
                        add = f"{tomb_left}{char}{tomb_right}\n"
                    else:
                        add = f"{tomb_left} {char} {tomb_right}\n"
                else:
                    add = f"{tomb_left}{char}{tomb_right}\n"
                result += add
            result += f"{tomb_left}{tomb_blank}{tomb_right}\n{tomb_bottom}"

            if len(result) <= 2000:
                break
            else:
                content_ = content_[:-1]
        return result

    if itrc:
        await itrc.response.send_message(create_tomb(content))
    elif ctx:
        await ctx.send(create_tomb(content))