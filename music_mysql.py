#!/usr/bin/python
# coding: utf-8

import MySQLdb
import music_comment
from music_name import name_list

music_comment.main()
# 因为python编码问题，数据库连接时，记得在后面添加 charset='utf8'
db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
tables_name = raw_input("请输入要编辑的数据表名称，不存在则新建表：")
cursor.execute("DROP TABLE IF EXISTS %s" % (tables_name))
netsqls = """CREATE TABLE %s (
            NAME VARCHAR(256),
            COMMENT INT,
            SONG_ID INT )""" % (tables_name)
cursor.execute(netsqls)
for i in range(len(name_list)):
    # 因为歌曲名称存在单引号冲突，所以用MySQLdb.escape_string转义
    sql = "INSERT INTO %s (NAME, COMMENT, SONG_ID) VALUES ('%s','%d', '%d')" % \
     (tables_name, MySQLdb.escape_string(music_comment.cm_na[0][i]), music_comment.cm_na[1][i], i)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
