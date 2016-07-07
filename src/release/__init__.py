import os

# argv1 = 'D:/task'
# argv2 = '20160607112619'
#
# # 调用命令行命令
# os.system('python dataInsertProcess.py {0} {1}'.format(argv1, argv2))

import urllib.request
import gzip
import io

# proxy_handler = urllib.request.ProxyHandler({'http': '220.249.185.178:9999'})
# opener = urllib.request.build_opener(urllib.request.HTTPHandler, proxy_handler)
# rsp = opener.open('http://esf.sh.fang.com/house/i331')
# str = rsp.read()
#
# if rsp.info().get('content-encoding') == 'gzip':
#     out_data = io.BytesIO(str)
#     gf = gzip.GzipFile(fileobj=out_data, mode='rb')
#     curr_page = gf.read().decode('gbk')
# else:
#     curr_page = str.decode('gbk')
#
# print(len(curr_page))
# opener.close()
# input()


argv1 = 'D:/task/xian'
argv2 = 'http://esf.gz.fang.com/house/i394'
argv3 = 'D:\\PycharmProjects\\NDCS\\src\\rule'
# argv4 = 30

os.system('python controlProcess.py {0} {1} {2}'.format(argv1, argv2, argv3))

# input()

