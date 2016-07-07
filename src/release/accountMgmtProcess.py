import socket
import null
import random


def get_proxy_address(item):
    addr = item[2: len(item)]
    return addr


def get_item_by_proxy_address(lst, addr):
    for item in lst:
        if str(item).find(addr) > 0:
            return item


# 代理地址文件路径
filePath = "../proxy/account.txt"
file = open(filePath, "r+", encoding='utf-8')
accountNum = len(file.readlines())
file.seek(0, 0)

# 代理账号列表（未分配）
proxyAccountList = []
# 已分配账号列表
assignedAccountList = []
# 失效账号列表
disabledAccountList = []

currItem = ""

# 遍历代理地址
for index in range(accountNum):
    proxyAccount = next(file)
    proxyAccount = str(proxyAccount).replace("\n", "")
    proxyAccountList.append(proxyAccount)

# 创建 socket 对象
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP和端口
host = '172.28.70.71'
port = 9999

# 绑定端口
if serverSocket != null:
    serverSocket.bind((host, port))

# 设置最大连接数，超过后排队
serverSocket.listen(10)

while True:
    # 建立客户端连接
    clientSocket, address = serverSocket.accept()

    reqData = clientSocket.recv(1024)
    reqData = str(reqData.decode('utf-8'))

    # 得到请求key
    splitIndex = reqData.index(',')
    key = reqData[0: splitIndex]

    # 账号分配
    if key == '1':
        # 得到随机账号
        accountCount = len(proxyAccountList)
        if accountCount == 0:
            clientSocket.send('0'.encode('utf-8'))
            continue

        idx = random.randint(0, len(proxyAccountList) - 1)
        currItem = proxyAccountList[idx]

        assignedAccountList.append(currItem)
        proxyAccountList.pop(idx)

        proxyAddr = get_proxy_address(currItem)
        clientSocket.send(proxyAddr.encode('utf-8'))
    # 账号返还
    elif key == '2':
        accountBack = reqData[splitIndex + 1: len(reqData)]
        item = get_item_by_proxy_address(assignedAccountList, accountBack)
        proxyAccountList.append(item)
        assignedAccountList.remove(item)


        msg = 'account returned'
        clientSocket.send(msg.encode('utf-8'))
    # 账号不可用，更换
    elif key == '-1':
        accountReplace = reqData[splitIndex + 1: len(reqData)]
        item = get_item_by_proxy_address(assignedAccountList, accountReplace)
        assignedAccountList.remove(item)

        tryTimes = int(item[0: 1])
        item = str(tryTimes - 1) + item[1: len(item)]
        if tryTimes > 1:
            proxyAccountList.append(item)
        else:
            disabledAccountList.append(item)

        # 得到随机账号
        accountCount = len(proxyAccountList)
        if accountCount == 0:
            clientSocket.send('0'.encode('utf-8'))
            continue

        idx = random.randint(0, len(proxyAccountList) - 1)
        currItem = proxyAccountList[idx]

        assignedAccountList.append(currItem)
        proxyAccountList.pop(idx)

        proxyAddress = get_proxy_address(currItem)
        clientSocket.send(proxyAddress.encode('utf-8'))
    elif key == 'exit':
        clientSocket.close()
        break
