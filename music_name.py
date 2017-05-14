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

id_list = []
name_list = []

def getsongsinfo():
    '''获取歌曲名称和id'''
    s = requests.session()
    s = BeautifulSoup(s.get(play_url,headers = headers).content, "lxml")
    song_xml = s.find('ul',{'class':'f-hide'})
    # 歌曲id爬取信息正则表达
    id_pattern = re.compile(r'id=(.*?)">')
    songs_id = id_pattern.findall(str(song_xml))
    for i in songs_id:
        id_list.append(int(i))
    # 歌曲名称爬取信息正则表达
    name_patterns = re.compile(r'\d+">(.*?)</a>')
    songs_name = name_patterns.findall(str(song_xml))
    for i in songs_name:
        name_list.append(i)
    # 列表打印出中文和日文等
    # return str(listsong).decode('string_escape')
getsongsinfo()
