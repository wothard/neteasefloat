#!/usr/bin/env python
# coding: utf-8

import MySQLdb
import re
# import uniout

db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
cursor = db.cursor()

for i in range(10):
	songs_list = []
	comments_list = []
	sql_value = "SELECT * FROM NETFLOATCT{} ".format(i)
	print sql_value
	try:
		print "ddd"
		cursor.execute(sql_value)
		results = cursor.fetchall()
		for i in range(len(results)):
			songs_list.append((results[i][0].encode('utf-8')))
			comments_list.append(int(results[i][1]))

	except:
	    print "Error : unable to fetch data!"

song_string = '['
comment_string = '['

# 检查歌曲是否有单引号
intro = "'"
# 将列表转化为字符串，
for i in range(19):
    # 检查歌曲是否有单引号
    if intro in songs_list[i]:
        pattern_intro = re.compile(r'\'')
        songs_list[i] = re.sub(pattern=pattern_intro, repl="\\'", string=songs_list[i])
    song_string += "'" + songs_list[i] + "'" + ", "
song_string += "'" + songs_list[19] + "'" + "]"
# 评论部分
for i in range(19):
    comment_string += str(comments_list[i]) + ", "
comment_string += str(comments_list[19]) + "]"

# 每次运行修改数据
song_name_data = re.compile(r'\[\'(.*?)\]')
song_comment_data = re.compile(r'\[\d(.*?)\]')

with open(r'data_file/index.htm', 'r') as f:
    html_content = f.read()
    changed_first = re.sub(pattern=song_name_data, repl=song_string, string=html_content)
    changed_last = re.sub(pattern=song_comment_data, repl=comment_string, string=changed_first)

with open(r'data_file/index.htm', 'w+')  as f2:
    f2.write(changed_last)
