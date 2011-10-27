
from zs.tools import pkcs7

class ModeOfOperationCBC (object):

    def __init__(self, BlockCipher, iv):
        self.block_cipher = BlockCipher()
        if len(iv) != self.block_cipher.block_size:
            raise ValueError("iv must be %d bytes long" %
                self.block_cipher.block_size)
        self.iv = iv

    @staticmethod
    def xor(a, b):
        return bytes(i ^ j for i, j in zip(a, b))

    def encrypt(self, data, key):
        b = self.block_cipher.block_size
        data, p, result = pkcs7.pad(data, b), self.iv, b''
        for i in range(len(data) // b):
            plain = data[i * b:i * b + b]
            ciph = self.block_cipher.encrypt(self.xor(plain, p), key)
            result, p = result + ciph, ciph
        return result

    def decrypt(self, data, key):
        b = self.block_cipher.block_size
        result, p = b'', self.iv
        for i in range(len(data) // b):
            ciph = data[i * b:i * b + b]
            plain = self.xor(self.block_cipher.decrypt(ciph, key), p)
            p = ciph
            result += plain
        pkcs7.check_padding(result, b)
        return pkcs7.unpad(result)
