# Cloud189
天翼云盘Mac端的Python实现

本项目是根据Mac下的天翼云盘应用通讯协议实现的

理论上可以实现断点续传，但还没做

下载因为我被限速了，所以没做，但是是能获取直链的，用axel/idm/aria2等工具都可以多线程下载

上传能达到我带宽的峰值，没啥问题


<h1 align="center">Cloud189</h1>

<p align="center">
<img src="https://img.shields.io/badge/version-2020.05.18-green.svg?longCache=true&style=for-the-badge">
<img src="https://img.shields.io/badge/license-GPLV3-blue.svg?longCache=true&style=for-the-badge">
</p>

<h4 align="center">⭐天翼云盘Mac端的Python实现⭐</h4>

<!-- <p align="center">
<img src="resources/demo.png" width="750">
</p> -->

## 功能

|组件                |版本           |描述                          |
|--------------------|---------------|------------------------------|
|login               |2020/5/18      |登录                           |
|list                |2020/5/18      |列目录                          |
|upload              |2020/5/18      |上传文件/文件夹                  |
|download            |2020/5/18      |获取下载链接                     |
|mkdir               |2020/5/18      |创建文件夹                      |
|rmdir               |2020/5/18      |删除文件夹                      |
|rmfile              |2020/5/18      |删除文件                        |
|share               |2020/5/18      |分享文件                        |


## 使用指南

### 源代码版本（推荐）

1. 克隆或[下载](https://github.com/Dawnnnnnn/Cloud189/archive/master.zip)本代码仓库

```
git clone https://github.com/Dawnnnnnn/bilibili-toolkit.git

```

2. 安装Python 3.6.5+，并使用pip安装依赖

```
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ 
```

3. 登录云盘

```
python3 main.py login 你的用户名 你的密码
```



## 用法

    本项目使用了Google Fire框架，因此您可以使用

    python3 main.py -h

    python3 main.py list -h

    等命令查看详细用法




#### 查看目录的文件
```bash
python3 main.py list --folder_id=文件夹id
(不传folder_id参数的情况下默认列出根目录，根目录id为-11)
```

#### 上传文件/文件夹
```bash
python3 main.py upload 文件路径 --parent_folder_id=文件夹id
(不传parent_folder_id参数的情况下默认为上传到根目录，根目录id为-11)
```

#### 获取下载文件直链
```bash
python3 main.py download --file_id=文件id
(file_id为必传参数)
```

#### 创建目录
```bash
python3 main.py mkdir --folder_id=父目录id --folder_name=新建目录的名称
(不传参数的情况下默认根目录，根目录id为-11，默认文件名为'新建文件夹')
```

#### 删除目录
```bash
python3 main.py rmdir --folder_id=要删除的文件夹id --folder_name=要删除的目录的名称
(folder_id和folder_name为必传参数)
```

#### 删除文件
```bash
python3 main.py rmfile --file_id=要删除的文件id --file_name=要删除的文件名称
(file_id和file_name为必传参数)
```

#### 分享文件
```bash
python3 main.py share --file_id=要分享的文件id
(不传参数的情况下默认列出根目录，根目录id为-11)
```

以上命令全部可以简写，比如

python3 main.py share 3154126670985214

python3 main.py list -13





## 错误

    一般来讲，只要参数无误，报错只有一种，是因为登录保存的accessToken失效了，重新登录就好了，自动登录下次一定做

## 鸣谢

本项目的灵感来自以下项目或作者：

> [cloud189](https://github.com/Aruelius/cloud189)
