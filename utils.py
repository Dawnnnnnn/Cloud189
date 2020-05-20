#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 00:08
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import hashlib
import hmac
import rsa
import base64
import os
import time
import inspect
import toml
from datetime import datetime

API_DOMAIN = 'https://api.cloud.189.cn'
UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) ????/1.0.0 ' \
            'Chrome/69.0.3497.128 Electron/4.2.12 Safari/537.36 '
SUFFIX_PARAM = 'clientType=TELEMAC&version=1.0.0&channelId=web_cloud.189.cn'
b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")
MAX_ATTEMPT_NUMBER = 3


def int2char(a):
    return BI_RM[a]


def b64tohex(a):
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if list(a)[i] != "=":
            v = b64map.index(list(a)[i])
            if 0 == e:
                e = 1
                d += int2char(v >> 2)
                c = 3 & v
            elif 1 == e:
                e = 2
                d += int2char(c << 2 | v >> 4)
                c = 15 & v
            elif 2 == e:
                e = 3
                d += int2char(c)
                d += int2char(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += int2char(c << 2 | v >> 4)
                d += int2char(15 & v)
    if e == 1:
        d += int2char(c << 2)
    return d


def calculate_md5_sign(params):
    return hashlib.md5('&'.join(sorted(params.split('&'))).encode('utf-8')).hexdigest()


def rsa_encode(j_rsakey, string):
    rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
    result = b64tohex((base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
    return result


def calculate_hmac_sign(secret_key, session_key, operate, url, date):
    request_uri = url.split("?")[0].replace(f"{API_DOMAIN}", "")
    plain = f'SessionKey={session_key}&Operate={operate}&RequestURI={request_uri}&Date={date}'
    return hmac.new(secret_key.encode(), plain.encode(), hashlib.sha1).hexdigest().upper()


def get_gmt_time():
    return datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


def get_file_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(64 * 1024)
            if not data:
                break
            md5.update(data)
        hash_md5 = md5.hexdigest()
    return hash_md5.upper()


def get_file_size(file_path):
    return str(os.path.getsize(file_path))


def get_file_name(file_path):
    return file_path.strip('/').strip('\\').rsplit('\\', 1)[-1].rsplit('/', 1)[-1]


def get_folder_name(file_path):
    return os.path.dirname(file_path).rsplit('\\', 1)[-1].rsplit('/', 1)[-1]


def printer(info, *args, end='\n'):
    format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    row = "[" + str(inspect.stack()[1][3]) + ":" + str(
        inspect.stack()[1][2]) + "]"
    if end != "\n":
        content = f'\r[{format_time}] {row} {info} {" ".join(f"{str(arg)}" for arg in args)}'
        print(content, flush=True, end=end)
    else:
        content = f'[{format_time}] {row} {info} {" ".join(f"{str(arg)}" for arg in args)}'
        print(content, flush=True, end=end)


def chunk_report(bytes_so_far, total_size):
    percent = int(float(bytes_so_far) / total_size * 100)
    printer(f"进度:{round(bytes_so_far / 1024 / 1024, 2)}/{round(total_size / 1024 / 1024, 2)}MB({percent}%)", end='')
    if bytes_so_far >= total_size:
        printer("")
