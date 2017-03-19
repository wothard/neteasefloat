#!/usr/bin/env python
#coding: utf-8
from gpcharts import figure
import musicc
import music

# 获取图像对象并设置x, y的值
fig3 = figure()
listz =[]
file = open ('htet.txt', 'r')
# while True:
#     line = file.readline()
#     if not line:
#         break
for line in file:
    listz.append(int(line))
file.close()
print listz[:20]


# music.songcomment()
# musicc.songname()
# xVals = ['R', '100']
# # # yVals = [['e','q','t','y','aa','ss','ccc'],[10,20,12,14,23,21,20]]
# yVals = [musicc.listsong[:30], music.commentaq[:30]]
# # yVals = [[listy],listx]
# fig3.title = 'qwe'
# fig3.ylabel = 'r'
# fig3.bar(xVals, yVals)
