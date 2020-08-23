import socket  # 导入 socket 模块

def client(time):
    s = socket.socket()  # 创建 socket 对象
    s.connect(('127.0.0.1', 8712))
    print(s.recv(1024).decode(encoding='utf8'))
    message = "我是"+str(time)+ "号，我已对接成功！"
    s.send(message.encode('utf8'))
    while True:
        print(s.recv(1024).decode(encoding='utf8'))
        m2 = input("")
        s.send(m2.encode('utf-8'))
client(1)

