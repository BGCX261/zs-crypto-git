
import random
system_random = random.SystemRandom()

print("--- do not use this module under any circumstances ---")

def mult_inv(a, b):
    ''' calculate the multiplicative inverse a**-1 % b ''' 
    # in addition to the normal setup, we also remember b
    last_b, x, last_x, y, last_y = b, 0, 1, 1, 0
    while b != 0:
        q = a // b
        a, b = b, a % b
        x, last_x = last_x - q * x, x
        y, last_y = last_y - q * y, y
    # and add b to x if x is negative
    if last_x < 0:
        return last_x + last_b
    return last_x

def generate_keys():
    q = int("ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129"
        "024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3"
        "cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7e"
        "c6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f"
        "24117c4b1fe649286651ece65381ffffffffffffffff", 16)
    g = 2
    x = system_random.randint(0, q - 1)
    h = pow(g, x, q)
    public_key, private_key = (q, g, h), (q, g, x)
    return public_key, private_key


def encrypt(m, public_key):
    q, g, h = public_key
    y = system_random.randint(0, q - 1)
    c1 = pow(g, y, q)
    c2 = ((m % q) * pow(h, y, q)) % q
    return c1, c2

def decrypt(c1, c2, private_key):
    q, g, x = private_key
    s = pow(c1, x, q)
    m_ = (c2 * mult_inv(s, q)) % q
    return m_

import time
t = time.time()
for i in range(100):
    public_key, private_key = generate_keys()
t = time.time() - t
print("generating keys: %04d ms" % ((t / 100) * 1000))


t_ = time.time()
for i in range(100):
    c1, c2 = encrypt(1337, public_key)
t_ = time.time() - t_
print("encrypting:      %04d ms" % ((t_ / 100) * 1000))
t__ = time.time()
for i in range(100):
    m = decrypt(c1, c2, private_key)
t__ = time.time() - t__
print("decrypting:      %04d ms" % ((t__ / 100) * 1000))
assert m == 1337























