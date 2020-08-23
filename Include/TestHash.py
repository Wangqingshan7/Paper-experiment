import hashlib
md5 = hashlib.md5()
md5.update(b"hello world")
print(md5.digest())
md51 = hashlib.md5()
md51.update(b'hello world')
print(md51.digest())
print(md5.digest_size)
print(md5.block_size)