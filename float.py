#!/usr/bin/env python
#coding: utf-8
from gpcharts import figure
import musicc
import music
import uniout

# 获取图像对象并设置x, y的值
fig3 = figure()
music.songcomment()
musicc.songname()
# print musicc.listsong[int(music.cl)-1:30+int(music.cl)-1]
# print len(musicc.listsong[int(music.cl)-1:30+int(music.cl)-1])
# print len(music.commentaq[:])
# print (music.commentaq[:])
xVals = ['Comment-numbers', 'Song-name']
# # yVals = [['e','q','t','y','aa','ss','ccc'],[10,20,12,14,23,21,20]]
yVals = [musicc.listsong[int(music.cl)-1:30+int(music.cl)-1], music.commentaq[:]]
fig3.title = 'netease歌曲评论图'
fig3.ylabel = ''
fig3.bar(xVals, yVals)
