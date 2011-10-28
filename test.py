
from zs.cipher import aes
from zs.password import pbkdf2
from zs.mmo import cbc
from zs.tools import pkcs7
from zs.tools import diffie_hellman

aes.test()
pbkdf2.test()
cbc.test()
pkcs7.test()
diffie_hellman.test()
