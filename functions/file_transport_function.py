#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 23:41
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from .operate_function import Operate
from utils import *
from xml.etree import ElementTree
import requests


class ChunkIO:

    def __init__(self, f, callback=None):
        self.f = f
        self.callback = callback

    def __iter__(self):
        count = 0
        for data in iter(self.f):
            count += len(data)
            yield data
            if self.callback:
                self.callback(count)

    def read(self, size=-1):
        return self.f.read(size)


class FileTransport:
    def __init__(self):
        self.config = toml.load('config.toml')
        self.sessionKey = self.config['account']['sessionKey']
        self.sessionSecret = self.config['account']['sessionSecret']
        self.operate = Operate()

    def download_file(self, file_id):
        url = f"{API_DOMAIN}/getFileDownloadUrl.action?fileId={file_id}&dt=3&shareId=&groupSpaceId=&short=0&{SUFFIX_PARAM}"
        date = get_gmt_time()
        headers = {
            "SessionKey": self.sessionKey,
            "Date": date,
            "Signature": calculate_hmac_sign(self.sessionSecret, self.sessionKey, 'GET', url, date),
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        node = ElementTree.XML(response.text)
        download_url = node.text
        download_url = requests.get(download_url, allow_redirects=False, verify=False).headers['Location']
        printer(f"下载链接(请使用axel/idm/aria2等工具进行直链下载):\n{download_url}")
        return download_url

    def create_upload_file(self, filepath, parent_folder_id=-11):
        for _ in range(MAX_ATTEMPT_NUMBER):
            try:
                url = f"{API_DOMAIN}/createUploadFile.action?{SUFFIX_PARAM}"
                date = get_gmt_time()
                headers = {
                    "SessionKey": self.sessionKey,
                    "Sign-Type": "1",
                    "User-Agent": UserAgent,
                    "Date": date,
                    "Signature": calculate_hmac_sign(self.sessionSecret, self.sessionKey, 'POST', url, date),
                    "Accept": "application/json;charset=UTF-8",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
                data = {
                    "parentFolderId": parent_folder_id,
                    "baseFileId": "",
                    "fileName": get_file_name(filepath),
                    "size": os.path.getsize(filepath),
                    "md5": get_file_md5(filepath),
                    "lastWrite": "",
                    "localPath": filepath,
                    "opertype": 1,
                    "flag": 1,
                    "resumePolicy": 1,
                    "isLog": 0
                }
                response = requests.post(url, headers=headers, data=data)
                upload_file_id = response.json()['uploadFileId']
                file_upload_url = response.json()['fileUploadUrl']
                file_commit_url = response.json()['fileCommitUrl']
                file_data_exists = response.json()['fileDataExists']
                printer(f"创建上传任务成功,上传节点为{file_upload_url.split('//')[1].split('.')[0]}")
                return upload_file_id, file_upload_url, file_commit_url, file_data_exists
            except Exception:
                pass

    def upload_file_data(self, file_upload_url, upload_file_id, filepath):
        url = f"{file_upload_url}?{SUFFIX_PARAM}"
        date = get_gmt_time()
        headers = {
            "SessionKey": self.sessionKey,
            "Edrive-UploadFileId": str(upload_file_id),
            "User-Agent": UserAgent,
            "Date": date,
            "Signature": calculate_hmac_sign(self.sessionSecret, self.sessionKey, 'PUT', url, date),
            "Accept": "application/json;charset=UTF-8",
            "Content-Type": "application/octet-stream",
            "Edrive-UploadFileRange": f"0-{os.path.getsize(filepath)}",
            "ResumePolicy": "1"
        }

        with open(filepath, "rb")as f:
            # response = requests.put(url=url, data=ChunkIO(f, callback=None), headers=headers)
            # printer(response.text)
            response = requests.put(url=url, data=f, headers=headers)
            if response.text != "":
                node = ElementTree.XML(response.text)
                if node.text == "error":
                    if node.findtext('code') != 'UploadFileCompeletedError':
                        printer(f"上传文件数据时发生致命错误{node.findtext('code')},{node.findtext('message')}")
            else:
                printer(f"上传文件{filepath}成功!")

    def upload_client_commit(self, file_commit_url, upload_file_id):
        for _ in range(MAX_ATTEMPT_NUMBER):
            try:
                url = f"{file_commit_url}?{SUFFIX_PARAM}"
                date = get_gmt_time()
                headers = {
                    "SessionKey": self.sessionKey,
                    "User-Agent": UserAgent,
                    "Date": date,
                    "Signature": calculate_hmac_sign(self.sessionSecret, self.sessionKey, 'POST', url, date),
                    "Accept": "application/json;charset=UTF-8",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
                data = {
                    "uploadFileId": upload_file_id,
                    "opertype": 1,
                    "isLog": 0,
                    "ResumePolicy": 1
                }
                response = requests.post(url, headers=headers, data=data)
                node = ElementTree.XML(response.text)
                if node.text != 'error':
                    printer(f"于[{node.findtext('createDate')}]上传文件[{node.findtext('name')}]({node.findtext('id')})成功")
                return True
            except Exception:
                pass

    def upload_file(self, filepath, parent_folder_id=-11):
        if os.path.isdir(filepath):
            dir_dict = {}
            printer(f'[{filepath}]是一个文件夹，开始解析目录结构')
            upload_files = []
            folder_name, folder_id, parent_folder_id = self.operate.mkdir(parent_folder_id, get_file_name(filepath))
            dir_dict[folder_name] = folder_id
            listdir = os.walk(filepath)
            for home, dirs, files in listdir:
                for file in files:
                    upload_files.append([f'{home}/{file}', dir_dict[get_folder_name(f'{home}/{file}')]])
                for i in range(0, len(dirs)):
                    dir = dirs[i]
                    if i == len(dirs) - 1:
                        folder_name, folder_id, parent_folder_id = self.operate.mkdir(folder_id, dir)
                        dir_dict[folder_name] = folder_id
                    else:
                        folder_name, id, pid = self.operate.mkdir(folder_id, dir)
                        dir_dict[folder_name] = id
            for upload_file in upload_files:
                printer(f"文件[{upload_file[0]}]进入上传流程")
                upload_file_id, file_upload_url, file_commit_url, file_data_exists = self.create_upload_file(
                    upload_file[0],
                    upload_file[1])
                if file_data_exists == 1:
                    printer('数据存在，进入秒传流程')
                    self.upload_client_commit(file_commit_url, upload_file_id)
                else:
                    self.upload_file_data(file_upload_url, upload_file_id, upload_file[0])
                    self.upload_client_commit(file_commit_url, upload_file_id)

        else:
            printer(f"文件[{filepath}]进入上传流程")
            upload_file_id, file_upload_url, file_commit_url, file_data_exists = self.create_upload_file(filepath)
            if file_data_exists == 1:
                printer('数据存在，进入秒传流程')
                self.upload_client_commit(file_commit_url, upload_file_id)
            else:
                self.upload_file_data(file_upload_url, upload_file_id, filepath)
                self.upload_client_commit(file_commit_url, upload_file_id)
