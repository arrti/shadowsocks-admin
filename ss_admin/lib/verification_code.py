#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti
# ref: https://segmentfault.com/a/1190000002978886

import random, os
from PIL import Image, ImageDraw, ImageFont


current_path = os.path.split(os.path.realpath(__file__))[0]

class VerificationCode(object):
    def __init__(self, font_color=(0, 0, 0),
                       font_size = 20,
                       font_path = current_path + '/SIMSUN.TTC',
                       size = (100, 40),
                       bg_color = (255, 255, 255, 255)):
        self.font_color = font_color
        self.font_size = font_size
        self.font_path = font_path
        self.font = ImageFont.truetype(self.font_path, self.font_size)
        self.size = size
        self.bg_color = bg_color
        self.image = Image.new('RGBA', self.size, self.bg_color)


    def __random_gb2312(self):
        empty = range(0xD7FA, 0xD7FF)
        val = 0xB0A1
        while 1:
            head = random.randint(0xB0, 0xD7) # 常用字
            body = random.randint(0xA1, 0xFE)
            val = (head << 8) | body
            if val not in empty:
                break
        str = "%x" % val
        return str.decode('hex').decode('gb2312', 'ignore')

    def __rotate(self):
        img1 = self.image.rotate(random.randint(-5, 5), expand=0)  # 默认为0，表示剪裁掉伸到画板外面的部分
        img = Image.new('RGBA', img1.size, (255,) * 4)
        self.image = Image.composite(img1, img, img1)

    def __random_rgb(self):
        return (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))

    def __random_point(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))

    def __random_line(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.__random_point(), self.__random_point()], self.__random_rgb())
        del draw


    def __draw_text(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw

    def generate(self, num = 4):
        gap = 5
        start = 0
        random_str = ''
        for i in range(0, num):
            char = self.__random_gb2312()
            random_str += char
            x = start + self.font_size * i + random.randint(0, gap) + gap * i
            self.__draw_text((x, random.randint(5, 10)), char, (0, 0, 0))
            self.__rotate()
        self.__random_line(8)
        return random_str, self.image
