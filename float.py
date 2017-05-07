#!/usr/bin/env python
#coding: utf-8
import MySQLdb
from gpcharts import figure
# import musicc
# import music
import uniout

# 获取图像对象并设置x, y的值
fig3 = figure()
songlist = []
commentlist = []

db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
cursor = db.cursor()
sql_value = "SELECT * FROM NETFLOATCT "
try:
    cursor.execute(sql_value)
    results = cursor.fetchall()

    for i in range(len(results)):
        songlist.append((results[i][0].encode('utf-8')))
        commentlist.append(int(results[i][1]))
except:
    print "Error : unable to fetch data!"
db.close()
# print songlist[:10]
# print (commentlist[:10])
xVals = ['Comment-numbers', 'Song-name']
# yVals = [['e','q','t','y','aa','ss','ccc'],[10,20,12,14,23,21,20]]
yVals = [songlist[:25], commentlist[:25]]
fig3.title = 'netease歌曲评论图'
fig3.ylabel = ''
fig3.bar(xVals, yVals)
