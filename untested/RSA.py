import random

def is_prime(n, k=50):
    '''
    Test whether n is prime using the probabilistic Miller-Rabin
    primality test. If n is composite, then this test will declare
    it to be probably prime with a probability of at most 4**-k.

    To be on the safe side, a value of k=64 for integers up to
    3072 bits is recommended (error probability = 2**-128). If
    the function is used for RSA or DSA, NIST recommends some
    values in FIPS PUB 186-3:

    <http://csrc.nist.gov/publications/fips/fips186-3/fips_186-3.pdf>

    '''
    def check_candidate(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(3, 2048):
        if n % i == 0:
            return False
    s = 0
    d = n - 1
    while True:
        q, r = divmod(d, 2)
        if r == 1:
            break
        s += 1
        d = q
    for i in range(k):
        a = random.randint(2, n - 1)
        if check_candidate(a):
            return False
    return True

def get_prime(bits):
    ''' Return a random prime up to 'bits' in length '''
    def check_size(n, bits):
        return len(bin(n)[2:]) == bits
    system_random = random.SystemRandom()
    while True:
        n = system_random.randint(0, 2 ** bits - 1)
        if check_size(n, bits) and is_prime(n):
            return n

def phi(n, p, q):
    ''' euler's totient function for n which can be written as pq'''
    return (n + 1) - (p + q)

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

def make_keys(bits=2048, e=65537):
    ''' Return two tuples, public and private key, as (n, e), (n, d) '''
    p, q = None, None
    while p == q:
        p, q = get_prime(bits // 2), get_prime(bits // 2)
    n = p * q
    print(len(hex(n)[2:]))
    phi_n = phi(n, p, q)
    d = mult_inv(e, phi_n)
    return (bits, n, e), (n, d, e)

def masked_pow(c, d, n, e):
    ''' calculates pow(c, d, n), but not as succeptible to timing attacks '''
    r = random.randint(1, n)
    return (pow((pow(r, e, n) * c) % n, d, n) * mult_inv(r, n)) % n


def encrypt(m, public_key):
    ''' encrypt an integer m with public key (n, e) '''
    bits, n, e = public_key
    if m > n:
        raise ValueError("input too large")
    return pow(m, e, n)

def decrypt(c, private_key):
    ''' decrypt an integer c with private key (n, d) '''
    n, d, e = private_key
    return masked_pow(c, d, n, e)


print("generating keys...\n")
public_key, private_key = make_keys(1024)
print("go...\n")
import time
t = time.time()
print(decrypt(encrypt(2**506, public_key), private_key))
print(2**506)
e = encrypt(2**510, public_key)
t = time.time()
for i in range(100):
    #print(i)
    assert decrypt(e, private_key) == 2**510
t = time.time() - t


print(t)
print("%.1f decryptions / second" % (1 / (t / 100)))


