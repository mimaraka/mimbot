from PIL import Image, ImageFont, ImageDraw, ImageFilter
import modules.img_utils as img_utils
import math
import numpy as np


class Mimbot_Image:
    image = 0

    def load(self, path):
        self.image = Image.open(path)

    def write(self, path):
        self.image.save(path)
    
    # ブラー
    def blur(self, values):
        if not values:
            return True
        elif values[0] == "box":
            radius = values[1] if len(values) > 2 else 10
            self.image = self.image.filter(ImageFilter.BoxBlur(radius=radius))
        elif values[0] == "gaussian":
            radius = values[1] if len(values) > 2 else 10
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=radius))
        elif values[0] == "median":
            size = values[1] if len(values) > 2 else 10
            self.image = self.image.filter(ImageFilter.MedianFilter(size=size))
        elif values[0] in ["maximum", "max"]:
            size = values[1] if len(values) > 2 else 10
            self.image = self.image.filter(ImageFilter.MaxFilter(size=size))
        elif values[0] in ["minimum", "min"]:
            size = values[1] if len(values) > 2 else 10
            self.image = self.image.filter(ImageFilter.MinFilter(size=size))
        elif values[0] == "radius":
            return False
        elif values[0] == "rank":
            size = values[1] if len(values) > 2 else 10
            rank = values[2] if len(values) > 3 else 5
            self.image = self.image.filter(ImageFilter.RankFilter(size=size, rank=rank))

        return False


    # 画像を変形
    def distort(self, values):
        # 波状に変形(波形ワープ)
        def wave(amp, freq, hor):
            width, height = self.image.size
            h1 = 0
            h2 = 0
            if hor:
                h1 = width
                h2 = height
            else:
                h1 = height
                h2 = width

            amp = amp / 100 * h1

            result = Image.new("RGB",self.image.size)

            #OpenCVはsizeではなくshape
            if len(values) > 3 and values[3] in ["hor", "horizontal"]:
                for y in range(self.image.size[1]):
                    for x in range(self.image.size[0]):
                        #for i in range(3):
                            #result[y, x][i] = img[y, roop(x + math.floor(amp * math.sin(y * freq / h2)), 0, img.shape[1] - 1)][i]
                        result.putpixel((x, y), tuple(self.image.getpixel((img_utils.roop(x + math.floor(amp * math.sin(y * freq / h2)), 0, self.image.size[0] - 1), y))))
            else:
                for y in range(self.image.size[1]):
                    for x in range(self.image.size[0]):
                        #for i in range(3):
                            #result[y, x][i] = img[roop(y + math.floor(amp * math.sin(x * freq / h2)), 0, img.shape[0] - 1), x][i]
                        result.putpixel((x, y), tuple(self.image.getpixel((x, img_utils.roop(y + math.floor(amp * math.sin(x * freq / h2)), 0, self.image.size[1] - 1)))))
            self.image = result

        # 渦状に変形
        def swirl(rot):
            return
        
        if not values:
            return True
        elif values[0] in ["wav", "wave"]:
            if len(values) > 3 and values[3] in ["horizontal", "hor"]:
                hor = 1
            else:
                hor = 0
            wave(float(values[1]), float(values[2]), hor)
            
        return False


    # エンボス
    def emboss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)


    # モザイク
    def mosaic(self, size=20):
        result = Image.new("RGB",self.image.size)
        tmp = np.zeros(((self.image.size[0] - 1)//size + 1, (self.image.size[1] - 1)//size + 1, 3), dtype = int)
        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                if (x, y) == ((x//size)*size, (y//size)*size):
                    for j in range((y//size)*size, img_utils.maxlim((y//size)*(size + 1), self.image.size[1])):
                        for i in range((x//size)*size, img_utils.maxlim((x//size)*(size + 1), self.image.size[0])):
                            for col in range(3):
                                tmp[x//size, y//size, col] += self.image.getpixel((i, j))[col]
                    for col in range(3):
                        tmp[x//size, y//size, col] //= size ** 2
                result.putpixel((x, y), tuple(tmp[x//size, y//size,:]))
        self.image = result


    # 画像のネガポジを反転
    def negative(self):
        result = Image.new("RGB",self.image.size)
        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                rgb = []
                for i in range(3):
                    rgb += [255 - self.image.getpixel((x, y))[i]]

                result.putpixel((x, y), tuple(rgb))
        self.image = result


    # ドット絵風
    def pixelize(self, size=20):
        result = Image.new("RGB",self.image.size)
        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                xx = (x//size)*size
                yy = (y//size)*size
                result.putpixel((x, y), tuple(self.image.getpixel((xx, yy))))
        self.image = result


    # テキストを追加
    def drawtext(self, text, pos, fill="white", anchor="mm", fontpath=".fonts/meiryo.ttf" , fontsize=24, direction="rtl", stroke_width=0, stroke_fill="black"):
        font = ImageFont.truetype(fontpath, fontsize)

        draw = ImageDraw.Draw(self.image)
        draw.text(pos, text, fill=fill, font=font, anchor=anchor, direction=direction, stroke_width=stroke_width, stroke_fill=stroke_fill)


    # コンポジット(透過画像対応)
    def composit(self, img, position):
        bg_clear = Image.new("RGBA", self.image.size, (255, 255, 255, 0))
        bg_clear.paste(img, position)
        self.image = Image.alpha_composite(self.image, bg_clear)