# -*- coding: cp936 -*-
from socket import *
from time import ctime


def serverSocket():
    HOST = '127.0.0.1'  # 主机地址
    PORT = 21567  # 服务器接收端口
    BUFSIZ = 1024  # 接收套接字的缓冲区大小
    ADDR = (HOST, PORT)  # 仅仅是将二者合起来，作为连接到的服务器地址类型

    tcpSerSock = socket(AF_INET, SOCK_STREAM)  # udpSerSock = socket(AF_INET , SOCK_DGRAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    while True:
        print('waiting for connection...')
        tcpCliSock, address = tcpSerSock.accept()
        print('connected from :', address)
        while True:
            recvData = tcpCliSock.recv(BUFSIZ)
            if not recvData:
                print('no found data')
                break
            tcpCliSock.send(('[%s] %s' % (ctime(), recvData)).encode('utf-8'))
            tcpCliSock.close()
    tcpSerSock.close()
def main():
    serverSocket()
if __name__ == '__main__':
    main()
