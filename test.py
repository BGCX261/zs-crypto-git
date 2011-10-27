
from zs.cipher import aes
from zs.mmo import cbc
from zs.password import pbkdf2

import os
iv = os.urandom(16)
m = cbc.ModeOfOperationCBC(aes.AES, iv)
print(m.decrypt(m.encrypt(b"hello world",
    b"aaaaaaaaaaaaaaaa"), b"aaaaaaaaaaaaaaaa"))

if __name__ == '__main__':
    aes.test()
    pbkdf2.test()
    print("all tests passed")
