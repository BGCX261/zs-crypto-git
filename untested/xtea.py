
import struct


def encrypt(block, key):
    s, d, m = 0, 0x9e3779b9, 0xffffffff
    key, (v0, v1) = struct.unpack(">4L", key), struct.unpack(">2L", block)
    for _ in range(32):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (s + key[s & 3]))) & m
        s = (s + d) & m
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (s + key[s >> 11 & 3]))) & m
    return struct.pack(">2L", v0, v1)

def decrypt(block, key):
    s, d, m = 0xc6ef3720, 0x9e3779b9 ,0xffffffff
    key, (v0, v1) = struct.unpack(">4L", key), struct.unpack(">2L", block)
    for _ in range(32):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (s + key[s >> 11 & 3]))) & m
        s = (s - d) & m
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (s + key[s & 3]))) & m
    return struct.pack(">2L", v0, v1)
