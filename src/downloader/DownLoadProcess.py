# -- coding: utf-8 --

# import sys
import os
import urllib.request
# import configparser
import hashlib
import json
import io
import urllib.parse, urllib.error
import gzip
import time
import random


# 下载网页函数 
def download_page_by_url(str_url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Connection': 'keep-alive'}

    req = urllib.request.Request(str_url, headers=header)
    rsp = urllib.request.urlopen(req)
    string = rsp.read()

    if rsp.info().get('content-encoding') == 'gzip':
        out_data = io.BytesIO(string)
        gf = gzip.GzipFile(fileobj=out_data, mode='rb')
        curr_page = gf.read().decode('gbk')
    else:
        curr_page = string.decode('gbk')
    return curr_page


# 保存网页函数
def save_page(new_file, str_url, curr_page):
    # print("文件名: ",  newFile.name)
    # fo.seek(0, 2)
    new_file.write(str_url)
    new_file.write(curr_page)
    new_file.close()
    return


# 得到md5值
def get_md5(str_url: str):
    md5 = hashlib.new('md5')
    md5.update(str_url.encode("utf-8"))
    return md5.hexdigest()


default_encoding = 'utf-8'
# if sys.getdefaultencoding() != default_encoding:
# reload(sys)
# sys.setdefaultencoding(default_encoding)


# 读取配置文件
with open("../downloader_conf.json", "r") as file:
    msg = json.load(file)

# 取得文件目录
urlPath = os.path.abspath('..') + "\\" + msg['URL_DIR']
downloadPath = os.path.abspath('..') + "\\" + msg['DOWNLOAD_DIR']

# 取得url文件列表
listFile = os.listdir(urlPath)
it = iter(listFile)

#  遍历url文件
for fileName in it:
    filePath = urlPath + "\\" + fileName
    file = open(filePath, "r+", encoding='utf-8')

    lineNum = len(file.readlines())
    file.seek(0, 0)

    # 遍历url地址
    for index in range(lineNum):
        url = str(next(file)).replace("\n", "")

        # 检查数据保存目录里是否存在已下载的网页文件
        fileNameMd5 = get_md5(url)
        downloadFilePath = downloadPath + "\\" + fileNameMd5 + ".txt"

        if os.path.exists(downloadFilePath):
            continue
        else:
            # 文件不存在则新建，并下载保存相关网页
            newF = open(downloadFilePath, 'w', encoding='utf-8')

            # 下载网页
            second = random.random() * 10
            time.sleep(second)
            page = download_page_by_url(url)
            # 保存网页
            save_page(newF, url, page)

    file.close()
