#!/usr/bin/env python
# coding: utf-8

from Crypto.Cipher import AES
import base64
import requests
import json
import codecs
import time
import uniout
import Queue
import threading
import re
from bs4 import BeautifulSoup

class TheKey(object):
    """用于解析评论动态加载的加密"""
    def __init__(self):
        self.nonce = "0CoJUm6Qyw8W8jud"
        self.nonce2 = 16 * 'F'
        self.modulus ="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.pubkey = '010001'
        self.encry_number = "0102030405060708"
    def aesEncrypt(self, text, nonce, encry_number):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(nonce, AES.MODE_CBC, self.encry_number)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text
    def page_params(self,page):
        '''判断多页评论，和多页评论的解析'''
        if page == 1:
            text = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            enText = self.aesEncrypt(text, self.nonce, self.encry_number)
        else:
            offset = str((page-1)*20)
            text = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset,'false')
            enText = self.aesEncrypt(text, self.nonce, self.encry_number)
        enText = self.aesEncrypt(enText, self.nonce2, self.encry_number)
        return enText

thekey = TheKey()

user_info_id = []
user_info_nickname = []
user_info_locate = []

class GetUserInfo(object):
    """获取在评论页提供的用户信息"""
    def __init__(self):
        self.headers = {
            'Host':"music.163.com",
            'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding':"gzip, deflate",
            'Content-Type':"application/x-www-form-urlencoded",
            'Cookie':"_ntes_nnid=754361b04b121e078dee797cdb30e0fd,1486026808627; _ntes_nuid=754361b04b121e078dee797cdb30e0fd; JSESSIONID-WYYY=yfqt9ofhY%5CIYNkXW71TqY5OtSZyjE%2FoswGgtl4dMv3Oa7%5CQ50T%2FVaee%2FMSsCifHE0TGtRMYhSPpr20i%5CRO%2BO%2B9pbbJnrUvGzkibhNqw3Tlgn%5Coil%2FrW7zFZZWSA3K9gD77MPSVH6fnv5hIT8ms70MNB3CxK5r3ecj3tFMlWFbFOZmGw%5C%3A1490677541180; _iuqxldmzr_=32; vjuids=c8ca7976.15a029d006a.0.51373751e63af8; vjlast=1486102528.1490172479.21; __gads=ID=a9eed5e3cae4d252:T=1486102537:S=ALNI_Mb5XX2vlkjsiU5cIy91-ToUDoFxIw; vinfo_n_f_l_n3=411a2def7f75a62e.1.1.1486349441669.1486349607905.1490173828142; P_INFO=m15527594439@163.com|1489375076|1|study|00&99|null&null&null#hub&420100#10#0#0|155439&1|study_client|15527594439@163.com; NTES_CMT_USER_INFO=84794134%7Cm155****4439%7Chttps%3A%2F%2Fsimg.ws.126.net%2Fe%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png.39x39.100.jpg%7Cfalse%7CbTE1NTI3NTk0NDM5QDE2My5jb20%3D; usertrack=c+5+hljHgU0T1FDmA66MAg==; Province=027; City=027; _ga=GA1.2.1549851014.1489469781; __utma=94650624.1549851014.1489469781.1490664577.1490672820.8; __utmc=94650624; __utmz=94650624.1490661822.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; playerid=81568911; __utmb=94650624.23.10.1490672820",
            'Connection':"keep-alive",
            'Referer':'http://music.163.com/'
        }
        self.proxies= {
            'http:':'http://121.232.146.184',
            'https:':'https://144.255.48.197'
        }
        self.encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    def getjson(self, url, params, encSecKey):
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        response = requests.post(url, headers=self.headers, data=data,proxies=self.proxies)
        return response.content
    def getuserinfo(self, url):
        '''获取评论页的用户名和评论'''
        params = thekey.page_params(1)
        encSecKey = self.encSecKey
        json_text = self.getjson(url,params,encSecKey)
        json_dict = json.loads(json_text)
        comments_num = int(json_dict['total'])
        if(comments_num % 20 == 0):
            page = comments_num / 20
        else:
            page = int(comments_num / 20) + 1
        print("共有%d页评论!" % page)
        for i in range(page):  # 逐页抓取
            params = thekey.page_params(i+1)
            encSecKey = self.encSecKey
            json_text = self.getjson(url,params,encSecKey)
            json_dict = json.loads(json_text)
            if i == 0:
                print("共有%d条评论!" % comments_num) # 评论总数
            for item in json_dict['comments']:
                # comment = item['content'] # 评论内容
                # likedCount = item['likedCount'] # 点赞数
                # comment_time = item['time'] # 评论时间
                userID = item['user']['userId'] # id
                nickname = item['user']['nickname'] # 昵称
                # avatarUrl = item['user']['avatarUrl'] # 头像地址
                user_info_id.append(unicode(userID))
                user_info_nickname.append(nickname)
            print("第%d页抓取完毕!" % (i+1))

class GetUserLocatetion(threading.Thread):
    """因为用户所在地在评论没有提供，只能去用户页面获取。
    因为从评论中可以获得所有用户id，所以直接使用多线程获取"""
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
        while True:
            url = self.queue.get()
            self.getlocatetion(url)
            self.queue.task_done()
    def getlocatetion(self, url):
        req = re.compile(r'<span>(.*?)</span>')
        s = requests.session()
        s = BeautifulSoup(s.get(url,headers=self.headers).content, "lxml")
        result = req.findall(str(s))
        if result[3] == '':
            result[3] = "None"
        user_info_locate.append(result[3])
        # print result[3]

def id_request():
    """主函数和定义线程数"""
    get = GetUserInfo()
    input_song_id = raw_input("请输入歌曲id： ")
    song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + input_song_id + "/?csrf_token="
    get.getuserinfo(song_url)
    urls = []
    for i in user_info_id:
        urlb = user_url = "http://music.163.com/user/home?id=%d" % (int(i))
        urls.append(urlb)
    # print urls
    queue = Queue.Queue()
    for url in urls:
        queue.put(url)
    for i in range(10):
        t = GetUserLocatetion(queue)
        t.setDaemon(True)
        t.start()
    queue.join()

# id_request()
