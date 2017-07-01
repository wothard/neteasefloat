#!/usr/bin/env python
# coding: utf-8

# import wordcloud
from wordcloud import WordCloud
from PIL import Image
import string
import random
import sys
import uniout
import music_name

def show(some):
    img = Image.open(r'data_file/some.png')
    iwidth, iheight = img.size
    # 创建词云图布局, 字体太大不上传
    # font = r'/home/wothard/neteasefloat/cabin-sketch-v1.02/zenhei.ttc'
    font = r'/home/wothard/neteasefloat/cabin-sketch-v1.02/CabinSketch-Bold.ttc'
    wc = WordCloud(
    collocations=False,
    font_path=font,
    width=iwidth, height=iheight,
    margin=1,
    background_color='black',
    font_step=1,
    random_state=False,
    prefer_horizontal=.9
    )
    # 创建且显示词云图,英文用generate()函数，中文用fit_words()函数
    # png = wc.generate(some)
    png = wc.fit_words(dict(some))
    png = png.to_image()
    for i in range(iwidth):
        for j in range(iheight):
            # getpixel第二个值决定将所对应的颜色添加词语(255,255,255)黑色，(0,0,0)白色
            if img.getpixel((i,j))[:3] == (0,0,0):
                # putpixel第二个值决定词云图背景色的颜色
                png.putpixel((i,j), (255,255,255))
    png.save(r'data_file/songnamecloud.png')

run_fuc = music_name.Main_Fuc()
run_fuc.main_run()

df = []
for i in music_name.name_list:
    df.append((i.decode('utf-8'),random.randint(1,2)))

show(df)
