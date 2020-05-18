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
    """
    登录模块，需传入用户名和密码
    :param username: 用户名
    :param password: 密码
    :return:
    """
    login = Login()
    login.login(username, password)


def upload(filepath, parent_folder_id=-11):
    """
    上传文件/文件夹模块
    :param filepath:文件路径(必选参数)
    :param parent_folder_id:父文件夹id(可选参数，默认为根目录)
    :return:
    """
    file_transport = FileTransport()
    file_transport.upload_file(filepath, parent_folder_id)


def download(file_id):
    """
    下载模块
    :param file_id: 文件id(必选参数)
    :return:
    """
    file_transport = FileTransport()
    file_transport.download_file(file_id)


def list(folder_id=-11):
    """
    列目录模块
    :param folder_id: 文件夹id(可选参数，默认为根目录)
    :return:
    """
    operate = Operate()
    operate.get_list_files(folder_id)


def mkdir(parent_folder_id=-11, folder_name='新建文件夹'):
    """
    新建文件夹模块
    :param parent_folder_id: 父文件夹id(可选参数，默认为根目录)
    :param folder_name: 新建文件夹名称(可选参数，默认为'新建文件夹')
    :return:
    """
    operate = Operate()
    operate.mkdir(parent_folder_id, folder_name)


def rmdir(folder_id, folder_name):
    """
    删除文件夹模块
    :param folder_id: 文件夹id(必选参数)
    :param folder_name: 文件名名称(必选参数)
    :return:
    """
    operate = Operate()
    operate.delete_folder(folder_id, folder_name)


def rmfile(file_id, file_name):
    """
    删除文件模块
    :param file_id: 文件id(必选参数)
    :param file_name: 文件名(必选参数)
    :return:
    """
    operate = Operate()
    operate.delete_file(file_id, file_name)


def share(file_id):
    """
    分享文件模块
    :param file_id: 文件id(必选参数)
    :return:
    """
    operate = Operate()
    operate.share(file_id)


if __name__ == '__main__':
    fire.Fire()
