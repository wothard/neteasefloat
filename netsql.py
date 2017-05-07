#!/usr/bin/python
#coding: utf-8

import MySQLdb
import music
import musicc

t = music.GetCommentNum()
t.songcomment()
musicc.songname()

cm = len(musicc.listx)
# 因为python编码问题，数据库连接时，记得在后面添加 charset='utf8'
db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS NETFLOATCT")
# netsqls = """CREATE TABLE NETFLOATCT (
            # NAME CHAR(128),
            # COMMENT INT )"""
# cursor.execute(netsqls)
for i in range(cm):
    sql = "INSERT INTO NETFLOATCT (NAME, COMMENT) VALUES ('%s',\
        '%d')" % (musicc.listsong[i], music.commentaq[i])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
