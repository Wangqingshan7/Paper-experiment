import threading #线程
import time
import socket

HOST = '127.0.0.1'  # 主机地址
PORT = 21567
threading_list = []
def client(i):
    s = socket.socket()
    s.connect((HOST,PORT))
    message = str(i)+"has set connection"
    s.send(message.encode('utf8'))

if __name__ == '__main__':
    for i in range(1):
        t = threading.Thread(target=client(i))
        threading_list.append(t)
    for x in threading_list:
        x.start()