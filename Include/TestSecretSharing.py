# from binascii import hexlify
# from binascii import unhexlify
# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
# from Crypto.Protocol.SecretSharing import Shamir
#
# key = get_random_bytes(16)
#
# shares = Shamir.split(2, 6, key)
# for idx, share in shares:
#     print("%d,%s" %(idx, hexlify(share)))
#print(shares[0])



# message = [(),()]
# shares.append((idx, unhexlify(share)))
# key = Shamir.combine(shares)






# from binascii import hexlify
# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
# from Crypto.Protocol.SecretSharing import Shamir
#
#
# message = '我是大帅哥!'
# key = message.encode('utf-8')
# print(key)
# shares = Shamir.split(2, 5, key)
# for idx, share in shares:
#     print("Index #%d: %s" % (idx, hexlify(share)))


from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir

#from sss import Shamir
message = '我是大帅哥!'
key = message.encode('utf-8')
print(key)
shares = Shamir.split(2, 5, key)
for idx, share in shares:
    print("Index #%d: %s" % (idx, hexlify(share)))



