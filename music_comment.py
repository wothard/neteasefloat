#!/usr/bin/env python
#coding: utf-8

import requests
import json
import os
import base64
import time
import threading
import Queue
from Crypto.Cipher import AES
from pprint import pprint
import hashlib
import music_name

class TheKey(object):
    """几个需要用到的解析网页js的函数"""
    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    def encryted_request(self, test):
        text = json.dumps(text)
        secKey = createSecretKey(16)
        encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
        encSecKey = rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        return data

theKey = TheKey()
comment_list = []
cm_na = []

class GetCommentNum(threading.Thread):
    '''获取每首歌曲的评论'''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.headers = {
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/'
        }
        self.text = {
            'username': '邮箱',
            'password': '密码',
            'rememberLogin': 'true'
        }
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'
        self.text = json.dumps(self.text)
        self.secKey = theKey.createSecretKey(16)
        self.encText = theKey.aesEncrypt(theKey.aesEncrypt(self.text, self.nonce), self.secKey)
        self.encSecKey = theKey.rsaEncrypt(self.secKey, self.pubKey,self. modulus)
        self.data = {
            'params': self.encText,
            'encSecKey': self.encSecKey
        }
        self.proxies = {
            'http': 'http://111.23.10.12',
            'https': 'https://219.153.76.70'
        }
    def run(self):
        while True:
            url = self.queue.get()
            # print self.name + ':' + 'begin post and get comments ...'
            # if lpp.acquire():
            self.getcomment(url)
                # lpp.release()
            self.queue.task_done()
            # print self.name + "get it completed! @_@"
    def getcomment(self, url):
        # 获取歌曲评论数
        req = requests.post(url, headers=self.headers, data=self.data, proxies=self.proxies)
        comment_list.append(req.json()['total'])

def main():
    urls = []
    cm_na.append(music_name.name_list)
    for i in range(143):
        urlo = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_name.id_list[i]) +'/?csrf_token='
        urls.append(urlo)
    queue = Queue.Queue()
    for url in urls:
        queue.put(url)
    for i in range(10):
        t = GetCommentNum(queue)
        t.setDaemon(True)
        t.start()
    queue.join()
    cm_na.append(comment_list)
if __name__ == '__main__':
    st = time.clock()
    main()
    sd = (time.clock() - st)
