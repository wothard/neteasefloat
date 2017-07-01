#!/usr/bin/env python
#coding: utf-8

import requests
import threading
from bs4 import BeautifulSoup
import re
import Queue
import uniout

headers = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

id_list = []
name_list = []

class GetAllAlbum(threading.Thread):
    """多线程获取歌手专辑"""
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.headers = headers
    def run(self):
        while 1:
            url = self.queue.get()
            self.getallalbum(url)
            self.queue.task_done()
    def getallalbum(self,url):
        '''获取歌曲名称和id'''
        s = requests.session()
        s = BeautifulSoup(s.get(url,headers=self.headers).content, "lxml")
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

class Main_Fuc(object):
    def __init__(self):
        self.urls = []
    def main_run(self):
        songs_id = raw_input("请选择：\n1.以歌手id获取热门50首歌曲\n2.以歌手id获取所有专辑\n3.以歌单id获取歌曲\n:")
        if int(songs_id) == 1:
            singer_id = raw_input("请输入id:")
            url = 'http://music.163.com/artist?id={}'.format(int(singer_id))
            self.getallalbum(url=url)
        elif int(songs_id) == 2:
            song_id = raw_input("请输入id:")
            url = 'http://music.163.com/artist/album?id={}'.format(int(song_id))
            self.thread_run(url=url)
        else:
            album_id = raw_input("请输入id:")
            url = 'http://music.163.com/playlist?id={}'.format(int(album_id))
            self.getallalbum(url=url)
    def thread_run(self,url):
        # 启用多线程
        self.get_album_by_page(url)
        queue = Queue.Queue()
        for urlt in self.urls:
            queue.put(urlt)
        for i in range(10):
            t = GetAllAlbum(queue)
            t.setDaemon(True)
            t.start()
        queue.join()
    def get_album_by_page(self,url):
        '''获取专辑的所有链接'''
        let_me = []
        first_album_page = requests.get(url,headers=headers).content
        page_pattern = re.compile(r'<a href="/artist/album\?id=\d+&limit=12&offset=(\d+)" class="zpgi">')
        album_pattern = re.compile(r'<a href="/album\?id=(\d+)" class="tit s-fc0">(.*?)</a>')
        result = page_pattern.findall(first_album_page)
        for i in range(len(result)):
            if i == 0:
                temp = album_pattern.findall(first_album_page)
                let_me.append(temp)
            album_url = "http://music.163.com/artist/album?id=10559&limit=12&offset=%s" % (result[i])
            con = requests.get(album_url,headers=headers).content
            id_all = album_pattern.findall(con)
            let_me.append(id_all)
        for i in let_me:
            for j in i:
                al_songs_url = "http://music.163.com/album?id=%s" % j[0]
                self.urls.append(al_songs_url)
    def getallalbum(self,url):
        '''获取歌曲名称和id'''
        s = requests.session()
        s = BeautifulSoup(s.get(url,headers=headers).content, "lxml")
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

# ins = Main_Fuc()
# ins.main_run()
