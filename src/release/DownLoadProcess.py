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
import socket
import sys

default_encoding = 'utf-8'


# if sys.getdefaultencoding() != default_encoding:
# reload(sys)
# sys.setdefaultencoding(default_encoding)


class SocketService:
    # IP和端口
    HOST = '172.28.70.71'
    PORT = 9999

    @staticmethod
    def get_socket():
        # 创建客户端socket对象
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务，指定主机和端口
        sk.connect((SocketService.HOST, SocketService.PORT))
        return sk


# 与代理账号Server交互
def request_for_server(req_info):
    tryTimes = 0
    while tryTimes < 3:
        # 得到socket
        client = SocketService.get_socket()

        # 发送信息请求服务端（key 1表示账号分配，2表示账号返还，-1表示账号更换）
        client.send(req_info.encode('utf-8'))

        # 接收小于1024 字节的数据
        rspMsg = client.recv(1024)

        if rspMsg.decode('utf-8') == '0':
            print('no account available, please try again later')
            time.sleep(10)
            tryTimes += 1
            req_info = "1,"
            client.close()
            continue
        tryTimes = 3
    return rspMsg.decode('utf-8')


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


# 下载网页函数(用代理方式)
def download_page_by_proxy(str_url, proxy_ip):
    proxy_handler = urllib.request.ProxyHandler({'http': proxy_ip})
    opener = urllib.request.build_opener(urllib.request.HTTPHandler, proxy_handler)
    rsp = opener.open(str_url)
    byte_html = rsp.read()

    if rsp.info().get('content-encoding') == 'gzip':
        out_data = io.BytesIO(byte_html)
        gf = gzip.GzipFile(fileobj=out_data, mode='rb')
        curr_page = gf.read().decode('gbk')
    else:
        curr_page = byte_html.decode('gbk')
    opener.close()
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


# 执行下载器功能
def do_download(task_path, start_url):
    # 读取配置文件
    with open("../downloader_conf.json", "r") as file:
        msg = json.load(file)

    # 创建任务文件目录
    # basePath = os.path.abspath('..') + os.sep + "task"
    # FORMAT_DATE = '%Y%m%d%H%M%S'
    # taskPath = root_path + os.sep + time.strftime(FORMAT_DATE)

    urlPath = task_path + os.sep + msg['URL_DIR']
    downloadPath = task_path + os.sep + msg['DOWNLOAD_DIR']

    # 创建文件目录
    if not os.path.exists(urlPath):
        os.mkdir(urlPath)
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)

    # 创建起始url文件
    FORMAT_DATE = '%Y%m%d%H%M%S'
    urlFilePath = urlPath + os.sep + time.strftime(FORMAT_DATE) + ".txt"
    fileUrl = open(urlFilePath, 'w', encoding='utf-8')
    fileUrl.write(start_url)
    fileUrl.write('\n')
    fileUrl.close()

    # 下载错误次数
    downloadErrorTimes = 0

    # 代理账号请求分配
    proxy_ip = request_for_server("1,")
    if proxy_ip == '0':
        print("----------------------------no account, download unfinished----------------------------------")
        return
    else:
        print('account assigned : ' + proxy_ip)
    counter = 0
    while counter < 10:
        if downloadErrorTimes >= 3:
            # 代理账号下载多次失败后请求更换
            proxy_ip = request_for_server("-1," + proxy_ip)
            if proxy_ip == '0':
                print("----------------------------no account, download unfinished----------------------------------")
                return
            else:
                print('account assigned : ' + proxy_ip)
                downloadErrorTimes = 0
                counter = -1

        # 取得url文件列表
        listFile = os.listdir(urlPath)
        it = iter(listFile)

        #  遍历url文件
        for fileName in it:
            filePath = urlPath + os.sep + fileName
            file = open(filePath, "r+", encoding='utf-8')

            lineNum = len(file.readlines())
            file.seek(0, 0)

            # 遍历url地址
            for index in range(lineNum):
                url = str(next(file)).replace("\n", "")

                # 检查数据保存目录里是否存在已下载的网页文件
                fileNameMd5 = get_md5(url)
                downloadFilePath = downloadPath + os.sep + fileNameMd5 + ".txt"

                if os.path.exists(downloadFilePath):
                    continue
                else:
                    # 下载网页
                    second = random.uniform(1, 5)
                    time.sleep(second)

                    # 普通方式下载
                    # page = download_page_by_url(url)

                    # 代理方式下载
                    try:
                        # proxy_ip = '106.38.251.62:8088'

                        page = download_page_by_proxy(url, proxy_ip)
                    except Exception as err:
                        print("proxy download error: {0}".format(err))
                        downloadErrorTimes += 1
                        continue

                    # 文件不存在则新建，并下载保存相关网页
                    newF = open(downloadFilePath, 'w', encoding='utf-8')

                    # 保存网页
                    save_page(newF, url, page)
                    print("downloaded: {0}".format(url))
                    # 重置
                    counter = -1
                    downloadErrorTimes = 0;
            file.close()
        if counter > -1:
            time.sleep(1)
        print('try {0}'.format(counter))
        counter += 1

    # 代理账号归还
    rspMsg = request_for_server("2," + proxy_ip)
    print(rspMsg)
    print("----------------------------download finished----------------------------------")


# 接收参数
taskPath = sys.argv[1]
startUrl = sys.argv[2]

# taskPath = 'D:\\task\\xian\\20160628093542'
# startUrl = 'http://esf.xian.fang.com/house/i398'

# 执行下载器
do_download(taskPath, startUrl)
input()
