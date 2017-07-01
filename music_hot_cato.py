#!/usr/bin/env python
# encoding: utf-8

import urllib
import re
import threading
import requests
import Queue
import pygal

province = []
injuries = []
class GetAllcolum(threading.Thread):
    """获取分类标签的所有歌单"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.headers = {
            'Referer':'http://music.163.com/',
            'Host':'music.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    def run(self):
        while 1:
            url = self.queue.get()
            self.getallcolum(url)
            self.queue.task_done()
    def getallcolum(self, url):
        req = requests.get(url, headers=self.headers).content
        filter_colum_name = re.compile(r'<a title="(.*?)class="msk"></a>')
        filter_play_number = re.compile(r'<span class="nb">(.*?)</span>')
        result0 = filter_colum_name.findall(req)
        result1 = filter_play_number.findall(req)
        for i in range(len(result1)):
            colum_name = result0[i].split('\"')
            colum_name = str(colum_name[0]).decode('string_escape')
            colum_name = colum_name.decode('utf-8')
            if '万' in result1[i]:
                i = result1[i].replace("万", "0000")
                injuries.append(int(i)/1000)
            else:
                injuries.append(int(result1[i])/1000)
            province.append(colum_name[:4])

def main():
    all_url = []
    queue = Queue.Queue()
    firsturl = raw_input('请输入音乐分类：')
    firsturl = urllib.quote(firsturl)
    first_url = 'http://music.163.com/discover/playlist/?cat=' + firsturl + '&order=hot'
    second_url = 'http://music.163.com/discover/playlist/?order=hot&cat=' + firsturl + '&limit=35&offset='
    all_url.append(first_url)
    for i in range(42):
        last_url = second_url + (str((i+1)*35))
        all_url.append(last_url)
    for url in all_url:
        queue.put(url)
    for i in range(10):
        t = GetAllcolum(queue)
        t.setDaemon(True)
        t.start()
    queue.join()
    # 制作成条形图（svg格式）
    line_chart = pygal.HorizontalBar()
    line_chart.title = u"网易云 "
    for i in range(len(injuries)):
        if injuries[i] > 100:
            line_chart.add(province[i], injuries[i])
    line_chart.render_to_file('data_file/music_hot_cato.svg')

main()
