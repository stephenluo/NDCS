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
import datetime
from bs4 import BeautifulSoup
import time


# print(sys.getdefaultencoding())

# url地址前缀
# prefixUrl = "http://esf.sh.fang.com"


# 取得标签子元素的数量
def get_element_count(chk_item: bs4.Tag) -> int:
    el_count = len(chk_item.find('p', class_='mt12').contents)
    return el_count


# 得到md5值
def get_md5(str_url: str):
    md5 = hashlib.new('md5')
    md5.update(str_url.encode("utf-8"))
    return md5.hexdigest()


# 执行解析器功能
def do_parse(task_path, rule_path):
    # 读取配置文件
    with open("../parser_conf.json", "r") as file:
        msg = json.load(file)

    # 取得文件目录
    urlPath = task_path + os.sep + msg['URL_DIR']
    downloadPath = task_path + os.sep + msg['DOWNLOAD_DIR']
    parserResultPath = task_path + os.sep + msg['PARSER_RESULT_DIR']
    # parserRulePath = os.path.abspath('..') + os.sep + msg['PARSER_RULE_DIR']

    # 创建文件目录
    if not os.path.exists(parserResultPath):
        os.mkdir(parserResultPath)

    # 解析规则文件
    dataRuleFilePath = rule_path + os.sep + "data_parser_rule.json"
    with open(dataRuleFilePath, encoding='utf-8') as f:
        dataRule = json.load(f)

    urlRuleFilePath = rule_path + os.sep + "url_parser_rule.json"
    with open(urlRuleFilePath, encoding='utf-8') as f:
        urlRule = json.load(f)

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

    # 变量定义
    nextPageUrl = ""

    counter = 0
    while counter < 10:
        try:
            # 取得download文件列表
            listFile = os.listdir(downloadPath)
            it = iter(listFile)

            # 遍历download文件
            for fileName in it:
                # url是否抓取标志
                urlSeizeFlg = 1

                filePath = downloadPath + os.sep + fileName
                file = open(filePath, "r+", encoding='utf-8')

                # 得到url
                url = file.readline()
                if url == "":
                    continue
                if url.replace("\n", "").endswith('100/'):
                    urlSeizeFlg = 0
                # 得到下载地址的Md5值
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
                    if urlSeizeFlg == 1:
                        try:
                            urlList = eval(listCmdUrl)
                            # 取下一页的地址
                            endIndex = url.index('/house')
                            prefixUrl = url[0: endIndex]
                            nextPageUrl = prefixUrl + eval(urlCmd)
                        except Exception as err:
                            print("解析url地址时error: {0}".format(err))
                            continue
                            # exit()

                    '''抓取楼盘数据'''
                    try:
                        houseList = eval(listCmd)
                    except Exception as err:
                        print("解析楼盘列表时error: {0}".format(err))
                        continue
                    # 定义解析结果集合
                    records = []
                    for item in houseList:
                        try:
                            hid = eval(idCmd)
                            ''' 得到抓取的楼盘信息 '''
                            estateName = eval(estateNameCmd)
                            estateAddress = eval(estateAddressCmd)

                            # 得到子元素的数量
                            elCount = get_element_count(item)
                            roomType = eval(roomTypeCmd) if elCount > 0 else ''
                            floor = ''
                            orientation = ''
                            buildingAge = ''

                            # 检查楼层，朝向和建筑年代是否存在
                            tmpData = eval(floorCmd) if elCount > 2 else ''
                            if get_field_name(tmpData) == 'floor':
                                floor = tmpData
                            elif get_field_name(tmpData) == 'orientation':
                                orientation = tmpData
                            elif get_field_name(tmpData) == 'building_age':
                                buildingAge = tmpData

                            tmpData = eval(orientationCmd) if elCount > 4 else ''
                            if get_field_name(tmpData) == 'floor':
                                floor = tmpData
                            elif get_field_name(tmpData) == 'orientation':
                                orientation = tmpData
                            elif get_field_name(tmpData) == 'building_age':
                                buildingAge = tmpData

                            tmpData = eval(buildingAgeCmd) if elCount > 6 else ''
                            if get_field_name(tmpData) == 'floor':
                                floor = tmpData
                            elif get_field_name(tmpData) == 'orientation':
                                orientation = tmpData
                            elif get_field_name(tmpData) == 'building_age':
                                buildingAge = tmpData

                            area = eval(areaCmd)
                            totalPrice = eval(totalPriceCmd) + "万"
                            unitPrice = eval(unitPriceCmd)
                        except Exception as err:
                            print("封装楼盘信息error: {0}".format(err))
                            continue

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

                # url地址保存
                if urlSeizeFlg == 1:
                    FORMAT_DATE = '%Y%m%d%H%M%S'
                    urlFilePath = urlPath + os.sep + time.strftime(FORMAT_DATE) + ".txt"
                    if os.path.exists(urlFilePath):
                        pass
                        # file = open(urlFilePath, 'a', encoding='utf-8')
                    else:
                        fileUrl = open(urlFilePath, 'w', encoding='utf-8')
                        fileUrl.write(nextPageUrl)
                        fileUrl.write('\n')
                        fileUrl.close()

                # 抓取数据保存
                encodeD = json.dumps(records, ensure_ascii=False)
                with open(parserResultFilePath, 'w', encoding='utf-8') as f:
                    f.write(encodeD)
                print("parsed: {0}".format(url.replace('\n', '')))

                # 重置
                counter = -1

                file.seek(0, 0)
                file.close()

            if counter > -1:
                time.sleep(2)
            counter += 1
        except Exception as err:
            counter += 1
            print("global error: {0}".format(err))
            time.sleep(1)

    print("----------------------------【parser finished】----------------------------------")


def get_field_name(value: str) -> str:
    if value == '':
        return ''

    if value.endswith('层'):
        return 'floor'
    elif value.endswith('向'):
        return 'orientation'
    else:
        return 'building_age'




# 接收参数
taskPath = sys.argv[1]
rulePath = sys.argv[2]

# taskPath = 'D:/task/20160613111111'
# rulePath = 'D:\\PycharmProjects\\NDCS\\src\\rule'

# 执行解析器
do_parse(taskPath, rulePath)
