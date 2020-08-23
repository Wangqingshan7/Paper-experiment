import rsa


(bob_pub,bob_pri) = rsa.newkeys(512)
print(f'公钥：{bob_pub}\n私钥：{bob_pri}\n')
message = 'hello world'.encode('utf-8')
crypto = rsa.encrypt(message,bob_pub)
print(f'密文：{crypto}',len(crypto))
message = rsa.decrypt(crypto,bob_pri)

print('解密后：', message.decode('utf-8'))