#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 01:54
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from utils import *
import requests


class Operate:
    def __init__(self):
        self.config = toml.load('config.toml')
        self.sessionKey = self.config['account']['sessionKey']
        self.sessionSecret = self.config['account']['sessionSecret']
        self.accessToken = self.config['account']['accessToken']

    def get_list_files(self, folder_id=-11):
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        url = f"{API_DOMAIN}/open/file/listFiles.action?pageSize=60&pageNum=1&folderId={folder_id}&iconOption=5&orderBy=lastOpTime&descending=true"
        params = f'AccessToken={self.accessToken}&Timestamp={timestamp}&pageSize=60&pageNum=1&folderId={folder_id}&iconOption=5&orderBy=lastOpTime&descending=true'
        headers = {
            "AccessToken": self.accessToken,
            "Sign-Type": "1",
            "User-Agent": UserAgent,
            "Sec-Metadata": "destination="", target=subresource, site=cross-site",
            "Timestamp": timestamp,
            "Signature": calculate_md5_sign(params),
            "Accept": "application/json;charset=UTF-8"
        }
        response = requests.get(url, headers=headers)
        msg = ("{:<70}{:^10}{:>10}".format(str('文件名'), str('文件id'), str('文件大小')))
        print(msg)
        for i in range(0, len(response.json()['fileListAO']['fileList'])):
            filename = response.json()['fileListAO']['fileList'][i]['name']
            file_id = response.json()['fileListAO']['fileList'][i]['id']
            file_size = response.json()['fileListAO']['fileList'][i]['size']
            msg = ("{:<70}{:^10}{:>10}MB".format(str(filename), str(file_id), str(round(file_size / 1024 / 1024, 2))))
            print(msg)

        msg = ("\n{:<80}{:<10}".format(str('文件夹名'), str('文件夹id')))
        print(msg)
        for j in range(0, len(response.json()['fileListAO']['folderList'])):
            dirname = response.json()['fileListAO']['folderList'][j]['name']
            dir_id = response.json()['fileListAO']['folderList'][j]['id']
            msg = ("{:<80}{:<10}".format(str(dirname), str(dir_id)))
            print(msg)

    def mkdir(self, parent_folder_id=-11, folder_name='新建文件夹'):
        for _ in range(MAX_ATTEMPT_NUMBER):
            try:
                timestamp = str(int(datetime.utcnow().timestamp() * 1000))
                url = f"{API_DOMAIN}/open/file/createFolder.action"
                params = f'AccessToken={self.accessToken}&Timestamp={timestamp}&parentFolderId={parent_folder_id}&folderName={folder_name}'
                headers = {
                    "AccessToken": self.accessToken,
                    "Sign-Type": "1",
                    "User-Agent": UserAgent,
                    "Sec-Metadata": "destination="", target=subresource, site=cross-site",
                    "Timestamp": timestamp,
                    "Signature": calculate_md5_sign(params),
                    "Accept": "application/json;charset=UTF-8"
                }
                data = {
                    "parentFolderId": parent_folder_id,
                    "folderName": folder_name
                }
                response = requests.post(url, headers=headers, data=data)
                printer(f'创建文件夹[{folder_name}]成功，文件夹id为[{response.json()["id"]}]，父文件夹id为[{parent_folder_id}]')
                return folder_name, response.json()["id"], parent_folder_id
            except Exception:
                pass

    def delete_folder(self, folder_id, folder_name):
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        task_infos = str([{"fileId": str(folder_id), "fileName": folder_name, "isFolder": 1}])
        url = f"{API_DOMAIN}/open/batch/createBatchTask.action"
        params = f'AccessToken={self.accessToken}&Timestamp={timestamp}&type=DELETE&taskInfos={task_infos}&targetFolderId='
        headers = {
            "AccessToken": self.accessToken,
            "Sign-Type": "1",
            "User-Agent": UserAgent,
            "Sec-Metadata": "destination="", target=subresource, site=cross-site",
            "Timestamp": timestamp,
            "Signature": calculate_md5_sign(params),
            "Accept": "application/json;charset=UTF-8"
        }
        data = {
            "type": 'DELETE',
            "taskInfos": task_infos,
            "targetFolderId": ""
        }
        response = requests.post(url, headers=headers, data=data)
        printer(f'删除文件夹[{folder_name}]状态:{response.json()["res_message"]}')

    def delete_file(self, file_id, file_name):
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        task_infos = str([{"fileId": str(file_id), "fileName": file_name, "isFolder": 0}])
        url = f"{API_DOMAIN}/open/batch/createBatchTask.action"
        params = f'AccessToken={self.accessToken}&Timestamp={timestamp}&type=DELETE&taskInfos={task_infos}&targetFolderId='
        headers = {
            "AccessToken": self.accessToken,
            "Sign-Type": "1",
            "User-Agent": UserAgent,
            "Sec-Metadata": "destination="", target=subresource, site=cross-site",
            "Timestamp": timestamp,
            "Signature": calculate_md5_sign(params),
            "Accept": "application/json;charset=UTF-8"
        }
        data = {
            "type": 'DELETE',
            "taskInfos": task_infos,
            "targetFolderId": ""
        }
        response = requests.post(url, headers=headers, data=data)
        printer(f'删除文件[{file_name}]状态:{response.json()["res_message"]}')

    def share(self, file_id):
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        url = f"{API_DOMAIN}/open/share/createShareLink.action?fileId={file_id}&expireTime=2099&shareType=1"
        params = f'AccessToken={self.accessToken}&Timestamp={timestamp}&fileId={file_id}&expireTime=2099&shareType=1'
        headers = {
            "AccessToken": self.accessToken,
            "Sign-Type": "1",
            "User-Agent": UserAgent,
            "Sec-Metadata": "destination="", target=subresource, site=cross-site",
            "Timestamp": timestamp,
            "Signature": calculate_md5_sign(params),
            "Accept": "application/json;charset=UTF-8"
        }
        response = requests.get(url, headers=headers)
        printer(
            f'创建分享链接成功，链接为[{response.json()["shareLinkList"][0]["url"]}]，提取码为[{response.json()["shareLinkList"][0]["accessCode"]}]')
