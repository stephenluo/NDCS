# -*- coding: utf-8 -*-
import hashlib
import sys
import gzip
import io
import json
import os
import re
import urllib.request
import urllib.error
import bs4.element
from bs4 import BeautifulSoup
import time

# print(sys.getdefaultencoding())

# url地址前缀
prefixUrl = "http://esf.sh.fang.com"


def get_element_count(chk_item: bs4.Tag) -> int:
    el_count = len(chk_item.find('p', class_='mt12').contents)
    return el_count


# 得到md5值
def get_md5(str_url: str):
    md5 = hashlib.new('md5')
    md5.update(str_url.encode("utf-8"))
    return md5.hexdigest()

# 读取配置文件
with open("../parser_conf.json", "r") as file:
    msg = json.load(file)

# 取得文件目录
urlPath = os.path.abspath('..') + os.sep + msg['URL_DIR']
downloadPath = os.path.abspath('..') + os.sep + msg['DOWNLOAD_DIR']
parserRulePath = os.path.abspath('..') + os.sep + msg['PARSER_RULE_DIR']
parserResultPath = os.path.abspath('..') + os.sep + msg['PARSER_RESULT_DIR']

# 解析规则文件
dataRuleFilePath = parserRulePath + os.sep + "data_parser_rule.json"
with open(dataRuleFilePath, encoding='utf-8') as file:
    dataRule = json.load(file)

urlRuleFilePath = parserRulePath + os.sep + "url_parser_rule.json"
with open(urlRuleFilePath, encoding='utf-8') as file:
    urlRule = json.load(file)

'''取解析规则配置文件值'''
# 数据解析规则
ruleNameData = dataRule['rule_name']
listCmd = dataRule['list']
idCmd = dataRule['data']['id']
estateNameCmd = dataRule['data']['items']['estate_name']
estateAddressCmd = dataRule['data']['items']['estate_address']
roomTypeCmd = dataRule['data']['items']['room_type']
floorCmd = dataRule['data']['items']['floor']
orientationCmd = dataRule['data']['items']['orientation']
buildingAgeCmd = dataRule['data']['items']['building_age']
areaCmd = dataRule['data']['items']['area']
totalPriceCmd = dataRule['data']['items']['total_price']
unitPriceCmd = dataRule['data']['items']['unit_price']

# url解析规则
ruleNameUrl = urlRule['rule_name']
listCmdUrl = urlRule['list']
urlCmd = urlRule['data']['url']

counter = 0
while counter < 3:
    # 取得download文件列表
    listFile = os.listdir(downloadPath)
    it = iter(listFile)

    # 遍历download文件
    for fileName in it:
        filePath = downloadPath + os.sep + fileName
        file = open(filePath, "r+", encoding='utf-8')

        # 得到下载地址的Md5值
        url = file.readline()
        fileNameMd5 = get_md5(url)

        parserResultFilePath = parserResultPath + os.sep + fileNameMd5 + ".json"
        # 检查是否解析过
        if os.path.exists(parserResultFilePath):
            continue
        else:
            # 结果文件不存在则新建，并保存结果数据
            html = file.read()
            soup = BeautifulSoup(html, "html.parser")

            '''抓取数据url地址'''
            urlList = eval(listCmdUrl)
            nextPageUrl = prefixUrl + eval(urlCmd)

            '''抓取楼盘数据'''
            houseList = eval(listCmd)
            # 定义解析结果集合
            records = []
            for item in houseList:
                hid = eval(idCmd)
                ''' 得到抓取的楼盘信息 '''
                estateName = eval(estateNameCmd)
                estateAddress = eval(estateAddressCmd)

                # 得到子元素的数量
                elCount = get_element_count(item)

                roomType = eval(roomTypeCmd) if elCount > 0 else ''
                floor = eval(floorCmd) if elCount > 2 else ''
                orientation = eval(orientationCmd) if elCount > 4 else ''
                buildingAge = eval(buildingAgeCmd) if elCount > 6 else ''

                area = eval(areaCmd)
                totalPrice = eval(totalPriceCmd) + "万"
                unitPrice = eval(unitPriceCmd)

                # print(hid + '->' + estate_name, roomType, floor, orientation, buildingAge, sep=',')

                # 抓取数据封装
                record = dict(data_name='houseInfo')
                record["id"] = hid

                items = dict()
                items["estate_name"] = estateName
                items["estate_address"] = estateAddress
                items["room_type"] = roomType
                items["floor"] = floor
                items["orientation"] = orientation
                items["building_age"] = buildingAge
                items["area"] = area
                items["total_price"] = totalPrice
                items["unit_price"] = unitPrice
                record["items"] = items
                records.append(record)

        # 文件读取(test)
        # parserResultFilePath = parserResultPath + "\\" + fileNameMd5 + ".json"
        # with open(parserResultFilePath, "r") as file1:
        #     msg = json.load(file1)
        # for item in msg:
        #     print(item["data_name"], item["id"])
        #     print(item["items"]["estate_name"], item["items"]["room_type"], item["items"]["building_age"])

        # url地址保存
        FORMAT_DATE = '%Y%m%d%H%M'

        urlFilePath = urlPath + os.sep + time.strftime(FORMAT_DATE) + ".txt"
        if os.path.exists(urlFilePath):
            file = open(urlFilePath, 'a', encoding='utf-8')
        else:
            file = open(urlFilePath, 'w', encoding='utf-8')
        file.write(nextPageUrl)
        file.write('\n')

        # 抓取数据保存
        encodeD = json.dumps(records, ensure_ascii=False)
        with open(parserResultFilePath, 'w', encoding='utf-8') as f:
            f.write(encodeD)

        # 重置
        counter = 0

    file.seek(0, 0)
    file.close()
    counter += 1
print("----------------------------parser finished----------------------------------")
