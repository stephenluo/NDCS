import os

# argv1 = 'D:/task'
# argv2 = '20160607112619'
#
# # 调用命令行命令
# os.system('python dataInsertProcess.py {0} {1}'.format(argv1, argv2))


argv1 = 'D:/task/beijing'
argv2 = 'http://esf.fang.com/house/i393'
argv3 = 'D:\\PycharmProjects\\NDCS\\src\\rule'
# argv4 = 30

os.system('python controlProcess.py {0} {1} {2}'.format(argv1, argv2, argv3))

input()

