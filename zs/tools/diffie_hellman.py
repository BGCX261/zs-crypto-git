''' Diffie-Hellman Key Exchange '''

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


import random


class DiffieHellman (object):

    def __init__(self, prime, generator, rand_max):
        self.p, self.g = prime, generator
        self.x = random.SystemRandom().randint(0, rand_max)

    def get_public_key(self):
        y = pow(self.g, self.x, self.p)
        return y

    def get_shared_secret(self, yb):
        key = pow(yb, self.x, self.p)
        return key


def test():

    try:
        from zs.tools import rfc3526
    except ImportError: 
        import rfc3526
    prime, generator = rfc3526.groups[2048]

    alice = DiffieHellman(prime, generator, 2**512)
    bob = DiffieHellman(prime, generator, 2**512)

    alices_secret = alice.get_shared_secret(bob.get_public_key())
    bobs_secret = bob.get_shared_secret(alice.get_public_key())

    assert alices_secret == bobs_secret
    print("diffie hellman: all tests passed")


if __name__ == '__main__':
    test()
