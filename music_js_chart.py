#!/usr/bin/env python
# coding: utf-8

import MySQLdb
from gpcharts import figure
import uniout

# 获取图像对象并设置x, y的值
fig3 = figure()
songs_list = []
comments_list = []

db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
cursor = db.cursor()
sql_value = "SELECT * FROM NETFLOATCT "
try:
    cursor.execute(sql_value)
    results = cursor.fetchall()
    for i in range(len(results)):
        songs_list.append((results[i][0].encode('utf-8')))
        comments_list.append(int(results[i][1]))
except:
    print "Error : unable to fetch data!"
db.close()
input = int(raw_input("目前有143，选择从第几首查看（每次查看25首）：")) - 1
xVals = ['Comment-numbers', 'Song-name']
yVals = [songs_list[input:30 + input], comments_list[input:30 + input]]
fig3.title = 'netease歌曲评论图'
fig3.ylabel = ''
fig3.bar(xVals, yVals)
