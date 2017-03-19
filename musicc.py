#!/usr/bin/env python
#coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import uniout

headers = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

play_url = 'http://music.163.com/playlist?id=128667671'

s = requests.session()
s = BeautifulSoup(s.get(play_url,headers = headers).content, "lxml")
main = s.find('ul',{'class':'f-hide'})

#歌曲爬取信息正则表达
pattern = re.compile(r'id=(.*?)</a>')
songs = pattern.findall(str(main))
#歌曲id
songid = re.compile(r'(\d+)">').findall(str(songs))

listx = []
for mcomment in songid:
    listx.append(int(mcomment))
# print listx
#歌曲名称
listsong = []
def songname():
    '''仅仅获取歌曲名称'''
    patterns = re.compile(r'\d+">(.*?)</a>')
    songss = patterns.findall(str(main))
    for i in songss:
        listsong.append(i)
    #列表打印出中文和日文等
    return str(listsong).decode('string_escape')
songnumbers = len(listsong)
if '__name__' == '__main__':
    songname()
