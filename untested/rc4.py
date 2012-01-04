
def key_schedule(key):
    s, j = bytearray(range(256)), 0
    for i in range(len(s)):
        j = (j + i + key[s[i] % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def key_stream(s):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        yield s[(s[i] + s[j]) % 256]

def encrypt(data, key):
    return bytes(i^j for i, j in zip(data, key_stream(key_schedule(key))))
decrypt = encrypt
