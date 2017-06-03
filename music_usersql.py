#!/usr/bin/env python
# coding: utf-8

import MySQLdb
from music_userlocate import id_request
from music_userlocate import user_info_id
from music_userlocate import user_info_locate
from music_userlocate import user_info_nickname


id_request()
db = MySQLdb.connect("localhost", "root", "ip16292132z", "netfloat", charset='utf8')
cursor = db.cursor()
tables_name = raw_input("请输入要编辑的数据表名称，不存在则新建表：")
cursor.execute("DROP TABLE IF EXISTS %s" % (tables_name))
netsqls = """CREATE TABLE %s (
            NAME_ID INT,
            NAME VARCHAR(256),
            LOCATE VARCHAR(256) )""" % (tables_name)
cursor.execute(netsqls)
for i in range(len(name_list)):
    # 因为歌曲名称存在单引号冲突，所以用MySQLdb.escape_string转义
    sql = "INSERT INTO %s (NAME_ID, NAME, LOCATE) VALUES ('%d','%s', '%s')" % \
     (tables_name, user_info_id[i], MySQLdb.escape_string(user_info_nickname), MySQLdb.escape_string(user_info_locate))
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
