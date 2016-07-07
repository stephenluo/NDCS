import socket
import time


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


tryTimes = 0
reqInfo = "-1,122.96.59.105:81"
while tryTimes < 5:
    # 得到socket
    client = SocketService.get_socket()

    # 发送信息请求服务端分配代理账号（key 1表示账号分配，2表示账号返还）
    client.send(reqInfo.encode('utf-8'))

    # 接收小于1024 字节的数据
    rspMsg = client.recv(1024)

    if rspMsg.decode('utf-8') == '0':
        print('没有可分配的账号，稍候再请求。')
        time.sleep(10)
        tryTimes += 1
        reqInfo = "1,"
        client.close()
        continue
    tryTimes = 5
    print(rspMsg.decode('utf-8'))


# # 发送信息请求服务端分配代理账号（key 1表示账号分配，2表示账号返还）
# reqInfo = "1,"
# client.send(reqInfo.encode('utf-8'))
# # 接收小于1024 字节的数据
# rspMsg = client.recv(1024)

# print(rspMsg.decode('utf-8'))



