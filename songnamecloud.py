#!/usr/bin/env python
#coding: utf-8

import wordcloud
from PIL import Image
import string
import random
import re
import musicc

def show(some):
    img = Image.open(r'/home/wothard/neteasefloat/some.jpg')
    iwidth, iheight = img.size
    #创建词云图布局
    wc = wordcloud.WordCloud(
    r'/home/wothard/neteasefloat/cabin-sketch-v1.02/CabinSketch-Bold.ttf',
    width=iwidth, height=iheight,
    background_color='black',
    font_step=3,
    random_state=False,
    prefer_horizontal=.9
    )
    #创建且显示词云图
    png = wc.generate(some)
    png = png.to_image()
    for i in range(iwidth):
        for j in range(iheight):
            # getpixel第二个值决定将所对应的颜色添加词语
            if img.getpixel((i,j))[:3] == (0,0,0):
                # putpixel第二个值决定词云图背景色的颜色
                png.putpixel((i,j), (255,255,255))
    png.save('songnamecloud.png')

# sometype = string.ascii_letters + string.digits + string.punctuation
# sometype = [''.join((random.choice(sometype) for i in range(8))) for j in range(650)]
# sometype = ''.join(sometype)
songstr = str(musicc.songsss).decode('string_escape')
pattern = re.compile(r'[,\']')
songstr = re.sub(pattern, r'', songstr)
show(songstr)