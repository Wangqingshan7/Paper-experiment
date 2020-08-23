
from sss import Shamir
p = Shamir.pol(5,b'sdasdasdsaadsada')
share = []
for i in range(5,10):
    share.append((i,Shamir.make_share(i,p)))
print(share)
key = Shamir.combine(share)
print(key)