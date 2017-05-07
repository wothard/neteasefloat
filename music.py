#!/usr/bin/env python
#coding: utf-8
import requests
import json
import os
import base64
from Crypto.Cipher import AES
from pprint import pprint
import hashlib
import requests
import musicc

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
commentaq = []

class GetCommentNum(object):
    def songcomment(self):
        headers = {
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/'
        }
        text = {
            'username': '邮箱',
            'password': '密码',
            'rememberLogin': 'true'
        }
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        text = json.dumps(text)
        secKey = theKey.createSecretKey(16)
        encText = theKey.aesEncrypt(theKey.aesEncrypt(text, nonce), secKey)
        encSecKey = theKey.rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        # 获取歌曲评论数
        print "你目前总共喜欢" + str(len(musicc.listx)) + "首歌曲"
        cm = len(musicc.listx)
        for i in range(cm):
            url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(musicc.listx[i]) +'/?csrf_token='
            req = requests.post(url, headers=headers, data=data)
            commentaq.append(req.json()['total'])

if '__name__' == '__main__':
    t = GetCommentNum()
    t.songcomment()
