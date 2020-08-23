from binascii import unhexlify
from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Protocol.SecretSharing import Shamir


# shares = []
# for x in range(2):
#     in_str = input("Enter index and share separated by comma: ")
#     for s in in_str.split(","):
#         idx, share = s
#         print("%d,%s" % (idx,share))
#         shares.append((idx, unhexlify(share)))
# key = Shamir.combine(shares)


shares = []
# for x in range(2):
#     in_str = input("Enter index and share separated by comma: ")
#     print(in_str.split(","))
#     (idx,share) = in_str.split(",")
#     print('%s,%s' % (idx, share))
        #idx = s[0]
        #share = s[1]
        #print('%d,%s' %(idx,share))
shares.append((1, unhexlify('d2a4ffb1ccfe1a475ff880b75298b570')))
shares.append((2, unhexlify('8ed04d48300c1a6357dfc8e08b858583')))
print(shares)
key = Shamir.combine(shares)
print(key)
print(key.decode('utf-8'))
