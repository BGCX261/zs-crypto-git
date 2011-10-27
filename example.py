
from zs.cipher import aes
from zs.mmo import cbc
from zs.tools import pkcs7
from zs.password import pbkdf2

import os
import hashlib

def encrypt(data, password):
    salt = os.urandom(64)
    key = pbkdf2.pbkdf2(hashlib.sha512, password.encode(), salt, 1000, 32)
    iv = os.urandom(16)
    mmo = cbc.ModeOfOperationCBC(aes.AES, iv)
    data = pkcs7.pad(data, 16)
    return salt, iv, mmo.encrypt(data, key)

def decrypt(data, password):
    try:
        salt, iv, data = data
        key = pbkdf2.pbkdf2(hashlib.sha512, password.encode(), salt, 1000, 32)
        mmo = cbc.ModeOfOperationCBC(aes.AES, iv)
        data = mmo.decrypt(data, key)
        pkcs7.check_padding(data, 16)
        return pkcs7.unpad(data)
    except ValueError:  # it's a good idea not to have chatty error messages
        pass
    raise ValueError("decryption error")

print(decrypt(encrypt(b"hello world", "password1"), "password1"))
