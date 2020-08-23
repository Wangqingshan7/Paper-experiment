import hashlib
import datetime
import base64
import socket
from sss import Shamir
from Crypto.Cipher import AES

class Vehicle:
    def __init__(self,pol,t,pse,key):
        """
        :param pol: Secret Sharing polynomial
        :param t: Secure coefficient producted by Certificate Authority
        :param Pse: Pseudonym
        :param key: Asymmetric key
        """
        self.pol = pol
        self.t = t
        self.pse = pse
        self.key = key

    #aes 加解密
    def aes_encode(self,data):
        while len(data) % 16 != 0:
            data += (16 - len(data) % 16) * chr(16 - len(data) & 16)
        data = str.encode(data)
        print(data)
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        return str(base64.encodebytes(aes.encrypt(data)), encoding='utf-8').replace('\n', '')
    def aes_decode(self,data):
        try:
            aes = AES.new(str.encode(self.key), AES.MODE_ECB)  # 初始化加密器
            decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf-8'))).decode('utf-8')  # 解密\
            print(decrypted_text.find(''))
            if decrypted_text.find('') == -1:
                pass
            else:
                decrypted_text = decrypted_text[:decrypted_text.find('')]
            print(decrypted_text)
        except Exception as e:
            pass
        return decrypted_text
    def aes_encodebyte(self,data):
        while len(data) % 16 != 0:
            data += (16 - len(data) % 16) * '\x00'.encode('utf-8')
        #print(data)
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        return str(base64.encodebytes(aes.encrypt(data)), encoding='utf-8').replace('\n', '')


    def establish_connection_and_send_message(self,b_data,message):
        '''
        :param data (a byte str): broadcast information from fog server
        :param message: the information which will be sended to fog server
        :return: if value if -1, the message has been be tempered
        '''
        de_data = self.validate_decrypt_message(b_data)
        index,ip,port = de_data.split(",")
        print(f'fog server parameters index：{index},ip:{ip},port:{port}')
        s = socket.socket()  # 创建 socket 对象
        s.connect((ip,int(port)))
        print(f'{ip} {port}的雾服务器已连接')
        m = self.generate_message(index,message)
        print(m)
        f_m = m[0].encode('utf-8')+m[1]
        print(f_m)
        s.send(f_m)
        # while True:
        #      print(s.recv(1024).decode(encoding='utf8'))
    def validate_decrypt_message(self,bytes):
        cipher_text = bytes[:-16].decode('utf-8')
        MAC = bytes[-16:]
        #print(cipher_text,MAC)
        plain_text = self.aes_decode(cipher_text)
        #print("明文为:",plain_text)
        #self.hash_model.update(plain_text.encode('utf-8'))
        md5 = hashlib.md5()
        md5.update(plain_text.encode('utf-8'))
        #print(self.hash_model.digest())
        if MAC == md5.digest():
            return plain_text
        else:
            return -1
    def generate_message(self,index,message):
        timestamp = datetime.datetime.now()
        F = Shamir.make_share(int(index), self.pol) + self.t.encode('utf-8')
        #print('length of F',len(F))
        m = message.encode('utf-8') + self.pse.encode('utf-8') + timestamp.isoformat().encode('utf-8')+self.t.encode('utf-8')+ F
        print("g_s print：",m)
        md5 = hashlib.md5()
        md5.update(m)
        MAC = md5.digest()
        #print('MAC:',MAC)
        return self.aes_encodebyte(m),MAC

    # def generate_meassage(index,message):
    #
    #     print("index:",index)
    #     print(type(index))
    #     F = Shamir.make_share(int(index),self.pol)
    #     print(F)
    #     m = message.encode('utf-8') +self.pse.encode('utf-8')+timestamp.isoformat().encode('utf-8')+ F
    #     #print(m)
    #     return m


if __name__ =="__main__":
    key = '1234561234561234'
    v1 = Vehicle(Shamir.pol(10,123456), '123', 'jack', key)
    broadcast_message = b'ay7eM3N9hyngbWdDBvxGe6HfHTL7MWzrOUW0u1XBjug=S\xed\xc9K\x862\x8ac\xe7\r\xfe\xb2\xb0i\xdb\x12'
    v1.establish_connection_and_send_message(broadcast_message,'hello world')



    # m = v1.generate_message(11, "hello world")
    # print(m)
    # m_b = m[0].encode('utf-8') + m[1]
    # print(m_b)
    #print(v1.validate_decrypt_message(m_b))
    #v1.aes_decode(m_b)
    #v1.establish_connection_and_send_message(broadcast_message, "hello world")
    #b'hello worldjack2020-03-02T21:54:26.212212\x04\xb4\x0f\x01w3$\xb8\x1a\xfd\xea\x8a4]+\xc7123'
    #cipherText = b"vGNerBda3Zc97KVW2qEwfTeyzkpp34GnBE5huqXe/Ui5zN/Bk2dBZJ9vdLxKtjXQWjObYhW/cwYA2WBtL0vetA=="
    #print(v1.aes_decode(cipherText))

    #print(v1.aes_decode(cipherText.decode('utf-8')))
    #print(v1.validate_decrypt_message(cipherText))
    # f_Object = Shamir.pol(10,123456)
    # print(generate_meassage(f_Object,11,'jack','hello world'))
    # print(f_Object)
    # shares = Shamir.make_share(11,f_Object)
    # print(shares)
    # shares1 = Shamir.make_share(2, f_Object)
    # shares2 = Shamir.make_share(3,f_Object)
    # print("shares:",shares)
    # print("shares1:", shares1)
    # print("shares2:", shares2
    # print(len(shares),len(shares1),len(shares2))
    #print(shares.decode('utf-8'))



    #
    #print(v1.generate_meassage(11,'hello'))
    #byte = b'+ULN4+1SDovcnltDAz+Krub32jmFqhVtYjA7aZOHyNHOjUSjEixaGO39QNQ8bE/n'
    #print(v1.aes_decode(byte.decode('utf-8')))
    #v1.aes_encode('hello')


    # byte = b'hello'
    # print(byte+b'\x00')


    #print(v1.aes_decode('9KcbkBKwtwv57qLJ0Drf5qHfHTL7MWzrOUW0u1XBjug='))
    #
    # if v1.establish_connection_and_send_message(broadcast_message,"hello world") == -1:
    #     print('消息验证错误')

    #v2 = Vehicle(Shamir.pol(10, 123456), 123, 'Tom', key, md5)
    #v2.establish_connection("9KcbkBKwtwv57qLJ0Drf5qHfHTL7MWzrOUW0u1XBjug=")
    #print(v1.generate_meassage('11',"hellowewewqaewaewae"))
    # print(v1.validate_decrypt_message(b'oPhrsD1cP7zK9fqX5u8Wt1EtWAmIJaacf0nE+HuMZSAeduDXdyWzN27NY2pBHyBQ^\xe0\xa4#u2\xa8O \xd9t\x80\xc9:\xb7\xb7'))