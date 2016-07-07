# -*- coding: utf-8 -*-
import sys
import os
import platform
import time
# from src.release import DownLoadProcess


# 获得平台操作系统
def getplatform():
    return platform.system()


# 接收参数
rootPath = sys.argv[1]
startUrl = sys.argv[2]
rulePath = sys.argv[3]



# 创建任务文件目录
FORMAT_DATE = '%Y%m%d%H%M%S'
parseTime = time.strftime(FORMAT_DATE)
taskPath = rootPath + os.sep + parseTime
if not os.path.exists(taskPath):
    os.mkdir(taskPath)

if getplatform() == 'Windows':
    # 下载数据
    os.system('start python DownLoadProcess.py {0} {1}'.format(taskPath, startUrl))
else:
    os.system('python DownLoadProcess.py {0} {1} &'.format(taskPath, startUrl))

# 解析数据
os.system('python parserProcess.py {0} {1}'.format(taskPath, rulePath))
# 保存到数据库
os.system('python dataInsertProcess.py {0} {1}'.format(rootPath, parseTime))



# # 执行下载和解析数据
# os.system('start python DownLoadProcess.py')
# os.system('start python parserProcess.py')
# parserProcess.do_parse()
