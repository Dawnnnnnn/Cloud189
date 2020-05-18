#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 23:28
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from functions.login_function import Login
from functions.file_transport_function import FileTransport
from functions.operate_function import Operate
import fire


def login(username, password):
    login = Login()
    login.login(username, password)


def upload(filepath, parent_folder_id=-11):
    file_transport = FileTransport()
    file_transport.upload_file(filepath, parent_folder_id)


def download(file_id):
    file_transport = FileTransport()
    file_transport.download_file(file_id)


def list(folder_id=-11):
    operate = Operate()
    operate.get_list_files(folder_id)


def mkdir(parent_folder_id=-11, folder_name='新建文件夹'):
    operate = Operate()
    operate.mkdir(parent_folder_id, folder_name)


def rmdir(folder_id, folder_name):
    operate = Operate()
    operate.delete_folder(folder_id, folder_name)


def rmfile(file_id, file_name):
    operate = Operate()
    operate.delete_file(file_id, file_name)


def share(file_id):
    operate = Operate()
    operate.share(file_id)


if __name__ == '__main__':
    fire.Fire()
