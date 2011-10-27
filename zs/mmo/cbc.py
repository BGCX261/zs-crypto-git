''' Cipher Block Chaining Mode of Operation '''

# Copyright (c) 2011, Stefano Palazzo <stefano.palazzo@gmail.com>

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


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
        if len(data) % b:
            raise ValueError("length of data must be divisible by %d" % b)
        p, result = self.iv, b''
        for i in range(len(data) // b):
            plain = data[i * b:i * b + b]
            ciph = self.block_cipher.encrypt(self.xor(plain, p), key)
            result, p = result + ciph, ciph
        return result

    def decrypt(self, data, key):
        b = self.block_cipher.block_size
        if len(data) % b:
            raise ValueError("length of data must be divisible by %d" % b)
        result, p = b'', self.iv
        for i in range(len(data) // b):
            ciph = data[i * b:i * b + b]
            plain = self.xor(self.block_cipher.decrypt(ciph, key), p)
            p = ciph
            result += plain
        return result


def test():
    print("cbc: no test implemented")
