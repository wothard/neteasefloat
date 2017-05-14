#!/usr/bin/python
# coding: utf-8

import MySQLdb
import music_comment

music_comment.main()
# 因为python编码问题，数据库连接时，记得在后面添加 charset='utf8'
db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS NETFLOATCT")
netsqls = """CREATE TABLE NETFLOATCT (
            NAME VARCHAR(256),
            COMMENT INT,
            SONG_ID INT )"""
cursor.execute(netsqls)
for i in range(143):
    # 因为歌曲名称存在单引号冲突，所以用MySQLdb.escape_string转义
    sql = "INSERT INTO NETFLOATCT (NAME, COMMENT, SONG_ID) VALUES ('%s','%d', '%d')" % \
     (MySQLdb.escape_string(music_comment.cm_na[0][i]), music_comment.cm_na[1][i], i)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
