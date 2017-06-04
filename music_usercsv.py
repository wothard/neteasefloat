#!/usr/bin/env python
# coding: utf-8

import csv
from music_userlocate import id_request
from music_userlocate import user_info_id
from music_userlocate import user_info_locate
from music_userlocate import user_info_nickname
import uniout

id_request()
# with open('user_locate.csv', 'wb') as cs:
# csvfile = file('user_locate.csv', 'wb')
# writer = csv.writer(csvfile)
# writer.writerow(['State', 'Comment'])
# writer.writerows(data)
# csvfile.close()
user_lo = []
for item in user_info_locate:
    result = item.split("：")
    if len(result) == 2:
        result = result[1].split("-")
        fuck = result[0].decode('utf-8')
        user_lo.append(fuck[:len(fuck)-1])
li =[u'广东省',u'山东省',u'福建省',u'青海省',u'湖北省',
     u'新疆',u'湖南省',u'江苏省',u'陕西省',u'河北省',
     u'安徽省',u'四川省',u'贵州省',u'山西省',u'西藏',
     u'浙江省',u'云南省',u'广西',u'宁夏',u'内蒙古',
     u'辽宁省',u'江西省',u'吉林省',u'黑龙江',u'河南省',
     u'海南省',u'甘肃省',u'北京市',u'天津市',u'上海市',
     u'重庆市',u'香港',u'澳门',u'台湾']
data = [('guang_dong',),('shan_dong',),('fu_jian',),('qing_hai',),('hu_bei',),
        ('xin_jiang',),('hu_nan',),('jiang_su',),('shan_xi_1',),('he_bei',),
        ('an_hui',),('si_chuan',),('gui_zhou',),('shan_xi_2',),('xi_zhang',),
        ('zhe_jiang',),('yun_nan',),('guang_xi',),('ning_xia',),('nei_meng_gu',),
        ('liao_ning',),('jiang_xi',),('ji_lin',),('hei_long_jiang',),('he_bei',),
        ('hai_nan',),('gan_su',),('bei_jing',),('tian_jin',),('shang_hai',),
        ('chong_qing',),('xiang_gan',),('ao_men',),('tai_wan',)]
li_data = [0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0,0,
           0,0,0,0]
for i in range(len(user_lo)):
    for j in range(len(li)):
        if user_lo[i] == li[j]:
            if user_lo.count(user_lo[i]) != li_data[j]:
                # print user_lo.count(user_lo[i])
                # data[j] += (str(user_lo.count(user_lo[i])),)
                li_data[j] = user_lo.count(user_lo[i])
for i in range(34):
    data[i] += (str(li_data[i]),)
# print data
with open(r'data_file/user_locate.csv', 'wb') as cs:
# csvfile = file('user_locate.csv', 'wb')
    writer = csv.writer(cs)
    writer.writerow(['State', 'Comment'])
    writer.writerows(data)
