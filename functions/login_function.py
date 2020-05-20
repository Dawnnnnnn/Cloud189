#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 23:38
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from urllib import parse
from utils import *
import requests
import re


class Login:
    def __init__(self):
        self.config = toml.load('config.toml')
        self.username = ""
        self.password = ""
        self.sessionKey = ""
        self.sessionSecret = ""
        self.accessToken = ""

    @staticmethod
    def get_prelogin_params():
        url = "https://cloud.189.cn/unifyLoginForPC.action?appId=8025431004&clientType=10020&returnURL=https://m.cloud.189.cn%2Fzhuanti%2F2020%2FloginErrorPc%2Findex.html&timeStamp=1589390130328"
        response = requests.get(url)
        param_id = re.findall(r'paramId = "(\S+)"', response.text, re.M)[0]
        req_id = re.findall(r'reqId = "(\S+)"', response.text, re.M)[0]
        return_url = re.findall(r"returnUrl = '(\S+)'", response.text, re.M)[0]
        captcha_token = re.findall(r"captchaToken' value='(\S+)'", response.text, re.M)[0]
        j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', response.text, re.M)[0]
        lt = re.findall(r'lt = "(\S+)"', response.text, re.M)[0]
        return param_id, req_id, return_url, captcha_token, j_rsakey, lt

    def login(self, username, password):
        param_id, req_id, return_url, captcha_token, j_rsakey, lt = self.get_prelogin_params()
        self.username = username
        self.password = password

        username = rsa_encode(j_rsakey, username)
        password = rsa_encode(j_rsakey, password)
        url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
        headers = {
            "User-Agent": UserAgent,
            "Referer": "https://open.e.189.cn/api/logbox/oauth2/unifyAccountLogin.do",
            "Cookie": f"LT={lt}",
            "X-Requested-With": "XMLHttpRequest",
            "REQID": req_id,
            "lt": lt
        }
        data = {
            "appKey": "8025431004",
            "accountType": "02",
            "userName": f"{{RSA}}{username}",
            "password": f"{{RSA}}{password}",
            "validateCode": "",
            "captchaToken": captcha_token,
            "returnUrl": return_url,
            "mailSuffix": "@189.cn",
            "dynamicCheck": "FALSE",
            "clientType": 10020,
            "cb_SaveName": 1,
            "isOauth2": 'false',
            "state": "",
            "paramId": param_id
        }
        response = requests.post(url, data=data, headers=headers, timeout=5)
        redirect_url = response.json()['toUrl']

        url = f"{API_DOMAIN}/getSessionForPC.action?redirectURL={parse.quote(redirect_url)}&{SUFFIX_PARAM}"
        headers = {
            "User-Agent": UserAgent,
            "Accept": "application/json;charset=UTF-8"
        }
        response = requests.get(url, headers=headers, timeout=5)
        self.sessionKey = response.json()['sessionKey']
        self.sessionSecret = response.json()['sessionSecret']
        self.accessToken = response.json()['accessToken']

        url = f"{API_DOMAIN}/open/oauth2/getAccessTokenBySsKey.action?sessionKey={self.sessionKey}"
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        params = f'AppKey=601102120&Timestamp={timestamp}&sessionKey={self.sessionKey}'
        headers = {
            "AppKey": '601102120',
            'Signature': calculate_md5_sign(params),
            "Sign-Type": "1",
            "Accept": "application/json",
            'Timestamp': timestamp,
        }
        response = requests.get(url, headers=headers, timeout=5)
        self.accessToken = response.json()['accessToken']
        self.config['account']['sessionKey'] = self.sessionKey
        self.config['account']['sessionSecret'] = self.sessionSecret
        self.config['account']['accessToken'] = self.accessToken
        self.config['account']['username'] = str(self.username)
        self.config['account']['password'] = str(self.password)
        with open("config.toml", "w")as f:
            toml.dump(self.config, f)
        printer(f"{self.config['account']['username']}登录成功")
        return self.sessionKey, self.sessionSecret, self.accessToken
