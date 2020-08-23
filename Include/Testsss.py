from binascii import hexlify
from sss import Shamir

"""
    Shamir's secret 
    (3,10)
"""
message = '我是大帅哥!'
key = message.encode('utf-8')
print(key)

n = 10
key_pol = Shamir.pol(3,key)
print("产生的多项式为：",key_pol)
shares = [(i, Shamir.make_share(i, key_pol)) for i in range(1,  n + 1)]

for idx, share in shares:
    print("Index #%d: %s " % (idx, hexlify(share)))