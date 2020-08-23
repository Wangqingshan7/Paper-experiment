import base64
from Crypto.Cipher import AES
import re
#解密
def aes_decode(data,key):
    try:
        aes = AES.new(str.encode(key),AES.MODE_ECB)  #初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data,encoding='utf-8')))  #解密\
        print(decrypted_text.find(''))
        if decrypted_text.find('') == -1:
            pass
        else:
            decrypted_text = decrypted_text[:decrypted_text.find('')]
        print(decrypted_text)
    except Exception as e:
        print(e)
    return decrypted_text

def aes_fog_decode(data,key):
    try:
        aes = AES.new(str.encode(key),AES.MODE_ECB)  #初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data,encoding='utf-8')))  #解密\
        print(decrypted_text)
        d = re.search(b'\x00',decrypted_text).span()
        decrypted_text = decrypted_text[:d[0]]
    except Exception as e:
        print(e)
    return decrypted_text

def aes_encode(data,key):
    while len(data)%16!=0:
        data +=(16-len(data)%16)*chr(16-len(data)&16)
    data = str.encode(data)
    aes = AES.new(str.encode(key),AES.MODE_ECB)
    return str(base64.encodebytes(aes.encrypt(data)),encoding='utf-8').replace('\n','')

if __name__ == '__main__':
    key = '1234561234561234'  #秘钥长度必须为16、24或32位，分别对应 AES-128、AES-192和AES-256

    #byte = b'vGNerBda3Zc97KVW2qEwfVJSdNDd9sqjuyoMCeWLzS/Lw0ADXADYqADFQX8fnGPg57WihjUmtey+yz3wOIq3jA=='

    #plaintext = 'hello worldjack2020-03-02T22:27:07.394994;l\xdeD\x16\t\xa2\xe7T\x92\xb5Q\xa0'\x85\xd7123'
    #print(b'\x00'.decode('utf-8'))
    byte = b'vGNerBda3Zc97KVW2qEwfWvixQHMAlOZwctn5XRxDTQqzbATD7KpEZpvTxb5/T4vDQBTC6Ee3WJy4+bUFrP8Og=='
    byte_str = byte.decode('utf-8')
    plaintext = aes_fog_decode(byte_str,key)
    print("解密值：",plaintext)
