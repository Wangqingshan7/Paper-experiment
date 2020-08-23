# -*- coding: cp936 -*-
from socket import *
from time import ctime


def serverSocket():
    HOST = '127.0.0.1'  # ������ַ
    PORT = 21567  # ���������ն˿�
    BUFSIZ = 1024  # �����׽��ֵĻ�������С
    ADDR = (HOST, PORT)  # �����ǽ����ߺ���������Ϊ���ӵ��ķ�������ַ����

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
