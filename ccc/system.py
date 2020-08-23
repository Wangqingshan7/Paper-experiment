

"""
    编码模式：utf-8
    哈希函数统一使用 MD5
    非对称加密：RSA
    对称加密：AES

    秘密恢复的准确率：
        Sharim secret sharing(t,n)

    交互过程
    追踪过程

"""
import hashlib
import datetime
import base64
from sss import Shamir
from Crypto.Cipher import AES


class Vehicle:
    def __init__(self,pol,t,Pse,key,md5):
        """
        :param pol: Secret Sharing polynomial
        :param t: Secure coefficient producted by Certificate Authority
        :param Pse: Pseudonym
        :param key: Asymmetric key
        :param md5: Hash model
        """
        self.pol = pol
        self.t = t
        self.Pse = Pse
        self.key = key
        self.md5 = md5

    def aes_encode(self,data):
        while len(data) % 16 != 0:
            data += (16 - len(data) % 16) * chr(16 - len(data) & 16)
        data = str.encode(data)
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        return str(base64.encodebytes(aes.encrypt(data)), encoding='utf-8').replace('\n', '')
    def aes_decode(self,data):
        try:
            aes = AES.new(str.encode(self.key), AES.MODE_ECB)  # 初始化加密器
            decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf-8'))).decode("utf-8")  # 解密
            decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]
        except Exception as e:
            pass
        return decrypted_text

    def SendToServer(self,fog,message):
        """
        :param fog: the purpose fog
        :param message: transmitted information
        :return: Cipher_text and MAC
        """
        timestamp = datetime.datetime.now()
        message = message + fog.index + timestamp.isoformat()
        print(message)
        self.md5.update(bytes(message,encoding="utf-8"))
        MAC = self.md5.digest()
        print(MAC)
        #final_message = message + str(MAC,encoding="utf-8")
        return self.aes_encode(message),MAC

    def ReciveFromServer(self):
        print('hello world')

class Fog:
    def __init__(self,index,M,key):
        self.index = index
        self.M = M
        self.key = key

    def SendToVehicle(self,vehicle,message):
        print("hello world")
    def ReciveFromVehicle(self,vehicle,):
        print("")

    #def interactionWithVehicle(self,vehicle):

#湘A.66666

if __name__ == "__main__":

    key = '1234561234561234'
    md5 = hashlib.md5()
    v1 = Vehicle(Shamir.pol(10,123456),123,'jack',key,md5)
    v2 = Vehicle()
    M=[]
    f1 = Fog('index1',M,key)
    print(v1.SendToServer(f1,'hello world'))