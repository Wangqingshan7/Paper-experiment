import hashlib
import time
import base64
import re
import socket  # 导入 socket 模块
from threading import Thread
from sss import Shamir
from Crypto.Cipher import AES

g_socket_server = None  # 负责监听的socket
g_conn_pool = []

class Fog:

    def __init__(self,index,M,key,ip,port,sum):
        """
        :param index: fog-server's index must be a inter
        :param M: a tuple stored the f(index) from different vehicle
        :param key: Asymmetric key
        :param hash_model: hash function
        :param ip: socket IP address
        :param port: socket port
        """
        self.index = index
        self.M = M
        self.key = key
        self.ip = ip
        self.port = port
        self.sum = sum

    #socket and threading
    def setSocketServer(self):
        """
            初始化fog服务端
        """
        ADDRESS = (self.ip, self.port)  # 绑定地址
        global g_socket_server
        g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        g_socket_server.bind(ADDRESS)
        g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
        print(f'IP：{self.ip} 端口：{self.port} 的雾服务端已启动，等待客户端连接...')
    def accept_client(self):
        """
        接收新连接
        """
        while True:
            client, address = g_socket_server.accept()  # 阻塞，等待客户端连接
            # 加入连接池
            #print('_ is here:',_)
            g_conn_pool.append(client)
            # 给每个客户端创建一个独立的线程进行管理
            thread = Thread(target=self.message_handle, args=(client,address))
            # 设置成守护线程
            thread.setDaemon(True)
            thread.start()
    def message_handle(self,client,address):
        """
        """
        print("sum：", self.sum)
        #client.sendall("Welcome,This FOG server".encode('utf-8'))
        while True:
            bytes = client.recv(1024)
            print("ciphertext:",bytes)
            if len(bytes) == 0:
                client.close()
                # 删除连接
                g_conn_pool.remove(client)
                print("有一个客户端下线了。")
                break
            else:
                s_t_v_d = time.clock()
                plaintext = self.validation_decrypt_message(bytes)
                e_t_v_d = time.clock()
                print("validation decrypt time:",e_t_v_d-s_t_v_d)
                self.sum += (e_t_v_d-s_t_v_d)
                if plaintext == -1:
                    print("来自", address, "客户端的消息验证错误...")
                    print("message:", bytes)
                else:
                    print("message from:", address, "content:", plaintext)

    #AES encrypt & decrypt
    def aes_encode(self,data):
        while len(data) % 16 != 0:
            data += (16 - len(data) % 16) * chr(16 - len(data) & 16)
        data = str.encode(data)
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        return str(base64.encodebytes(aes.encrypt(data)), encoding='utf-8').replace('\n', '')
    def aes_decode(self,data):
        try:
            aes = AES.new(str.encode(self.key), AES.MODE_ECB)  # 初始化加密器
            decrypted_text = aes.decrypt(base64.decodebytes(data)).decode("utf-8")  # 解密
            if decrypted_text.find('') == -1:
                pass
            else:
                decrypted_text = decrypted_text[:decrypted_text.find('')]
        except Exception as e:
            pass
        return decrypted_text

    def aes_encodebyte(self,data):
        while len(data) % 16 != 0:
            data += (16 - len(data) % 16) * ''.encode('utf-8')
        #print(data)
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        return str(base64.encodebytes(aes.encrypt(data)), encoding='utf-8').replace('\n', '')
    def aes_decodebyte(self,data):
        try:
            aes = AES.new(str.encode(self.key), AES.MODE_ECB)  # 初始化加密器
            decrypted_text1 = aes.decrypt(base64.decodebytes(data)).decode('utf-8') # 解密
            #print(decrypted_text1)
            if decrypted_text1.find('') == -1:
                pass
            else:
                decrypted_text1 = decrypted_text1[:decrypted_text1.find('')]
        except Exception as e:
            pass
        return decrypted_text1

    def aes_re_decode(self,data):
        try:
            aes = AES.new(str.encode(self.key), AES.MODE_ECB)  # 初始化加密器
            decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf-8')))  # 解密\
            #print(decrypted_text)
            d = re.search(b'\x00', decrypted_text).span()
            #print(d)
            decrypted_text = decrypted_text[:d[0]]
            #print("cutted:",decrypted_text)
        except Exception as e:
            print(e)
        return decrypted_text

    # broadcast ip、port、index to vehicle
    def broadcast_to_vehicle(self):
        f=open(r"C:\Users\WangQingShan\Desktop\test1.txt", 'r', encoding='utf-8')
        memssage = f.read()
        f.close()

        info = str(self.index) +','+self.ip+','+str(self.port) + memssage
        #print(info)
        md5 = hashlib.md5()
        md5.update(info.encode('utf-8'))
        MAC = md5.digest()
        ct = self.aes_encode(info)
        return ct.encode('utf-8')+MAC

    def validation_decrypt_message(self,bytes):
        cipher_text = bytes[:-16].decode('utf-8')
        MAC = bytes[-16:]
        #print(cipher_text,MAC)
        plain_text = self.aes_re_decode(cipher_text)
        #print("明文为:",plain_text)
        md5 = hashlib.md5()
        md5.update(plain_text)
        #print(md5.digest())
        if MAC == md5.digest():
            return plain_text
        else:
            return -1


if __name__ == "__main__":
    M = {}
    key = '1234561234561234'
    fog1 = Fog(11,M,key,'127.0.0.3',8712,0.0)

    # message = b'u1fHW/q3cySD8qeK6/DuPlCQPAJ2XSbGNQrbKvybuVbPqItHcjLrtsqQPMYtcu7eKumHSu0WP6BCOVJ8v+wydOWNKv/vD65jdSseZAd/qMmg94FbRnHoNgFbSO0Wf5sQ42svcwoPQKvwoy3rjIXMUeEJAr7mld34w0esnKkrhvGM2P3CBBco32igN3g3VyoU0HpQ6OcuMf55rIFlMoYf03SU9iuhuGfpBs3G9IQ3AwKIsMPfWIqsUtP1v23eSXnC4as6sBm7nsBOHCZBYx+NAiw0OpX2a0rWwe3QIIkE5D4NzWIaVl7FqYPcKqnAIVvegUE1Nhfl+c6naYT1VnmBF3Rq6LxW4NYfewe0D8JQsTSbLsKtH6n+idjGA9LtAX+OCP1ryhgL46Ffy/Z1BJw4y2ciaiuBmMpc9fUtMvmZSPt/a3pAqz8O0DAyJ1yh/Zzs+uoHlULtgZNka0I67bQtNl7FeaPPZMwtlyfqng9obKQCNjemt6g10psqp2M+phacSsjy/qxMP6YX1HWIE9d9kn6WB/tF0kZXDojDQ0nV1WRg7v5e5cGrpQ42zGfK4JWo4WPYg0YpRlylimCy2ysyTgf+g5Q/tSRCu8IahKnmBkPqwDB5VSenAg6tSNAy03538axVsolL0tk5BcNcdd+aftDOrV+UIhEAtU4NHvOTma9X2HdkmfbLQnbcjn2J60Qp6i7UISAM/gSInU6nAR2lKA==\xde\xce\xe0=\x94\x84!_EF\x05\xc5\\\x8dT\x9e'
    # print(fog1.validation_decrypt_message(message))
    # f = open(r"C:\Users\WangQingShan\Desktop\test1.txt", 'r', encoding='utf-8')
    # message1 = f.read()
    # print(message)
    # f.close()
    # message1 = b"Interaction requests are often closely linked to people's private information. If the interactive request can be uniquely linked to the vehicle, private information (such as license plate information or owner information) may be leaked, and such private information must not be obtained by illegal organizations. Even though some pseudonyms schemes and cryptographic-based interaction methods have achieved better privacy protection in IoV, they have not considered internal attacks, \npse12020-03-05T14:53:25.615295231\x00\xb0\xee\x1dT\xcfq\xac\x95\x98Q\x04C\r\xd4\x0e231"
    # md5 = hashlib.md5()
    # md5.update(message)
    # print(md5.digest())


    start_time_b_m = time.clock()
    print("broadcast message:",fog1.broadcast_to_vehicle())
    end_time_b_m = time.clock()
    print('product time of b_m',end_time_b_m - start_time_b_m)
    fog1.setSocketServer()
    thread = Thread(target=fog1.accept_client)
    #print("test")
    thread.setDaemon(True)
    #print("test1")
    thread.start()
    #print("test2")


    while True:
        cmd = input("1:查看当前在线人数和详细信息 2:给指定客户端发送消息 3:查看时间开销 4:关闭服务器---请输入：")
        if cmd == '1':
            print("当前在线人数：",len(g_conn_pool))
            if len(g_conn_pool) == 0:
                pass
            else:
                for i in range(len(g_conn_pool)):
                    print("index:",i,'--',g_conn_pool[i])
                    #print(type(g_conn_pool[i]))
                    #print(g_conn_pool[i]._)
        elif cmd == '2':
            index, msg = input("请输入“索引,消息”的形式：").split(",")
            g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
        elif cmd == '3':
            print("sum time:",fog1.sum)
        elif cmd == '4':
            exit()

    # #
    # #print(fog1.broadcast_to_vehicle())