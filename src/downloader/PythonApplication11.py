# -- coding: utf-8 --
# -*- coding: cp-1252 -*-

import sys
import urllib.request
import os
import configparser

# print(sys.stdout.encoding)
# print(sys.getdefaultencoding())
# print(sys.getfilesystemencoding())


# for x in range(1, 5):
#    print(x, sep=',', end = '\n')

# x = "this ""is "    "string"

cf = configparser.ConfigParser()
cf.read("config.conf")

s = cf.sections()
print("section", s)

input("111")

response = urllib.request.urlopen('http://python.org/')

html = response.read()
html = html.decode('utf-8')			# Decoding the binary data to text.

html = "http://www.baidu.com\n" + html

n = len(html)


# 打开文件
fo = open("url\\tt.txt", "r+",  encoding='utf-8')
# os.open(

print("文件名: ",  fo.name)

# str = "6:www.runoob.com"
# 在文件末尾写入一行
# fo.seek(0, 2)

line = fo.write(html)

# 读取文件所有内容
fo.seek(0, 0)
for index in range(5):
    line = next(fo)
    print("文件行号 %d - %s" % (index, line))

# 关闭文件
fo.close()
