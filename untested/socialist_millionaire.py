
import hashlib
import json
import random
import gzip

class SocialistMillionaireError (Exception):

    pass


class SocialistMillionaire (object):

    _g1536 = int("""
      FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
      29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
      EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
      E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
      EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
      C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
      83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
      670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF
    """.replace(" ", "").replace("\n", ""), 16)

    def __init__(self, secret):
        self.p, self.g1 = self._g1536, 2
        self.__secret = int(hashlib.sha512(secret).hexdigest(), 16)
        self.__random = random.SystemRandom()

    @staticmethod
    def pw(b, e, m):
        ''' calculate pow(b, e, m) - works if e is negative '''
        def mult_inv(a, b):
            ''' calculate the multiplicative inverse a**-1 % b '''
            last_b, x, last_x, y, last_y = b, 0, 1, 1, 0
            while b != 0:
                q = a // b
                a, b = b, a % b
                x, last_x = last_x - q * x, x
                y, last_y = last_y - q * y, y
            if last_x < 0:
                return last_x + last_b
            return last_x
        if e >= 0:
            return pow(b, e, m)
        d = mult_inv(b, m)
        return pow(d, abs(e), m)

    @staticmethod
    def dump(*a):
        return gzip.compress(json.dumps(a).encode())

    def load(self, j):
        return tuple(json.loads(gzip.decompress(j).decode()))

    def start(self):
        pw = self.pw
        a2 = self.a2 = self.__random.randint(1, 2**1536)
        a3 = self.a3 = self.__random.randint(1, 2**1536)
        g2a = pw(self.g1, a2, self.p)
        g3a = pw(self.g1, a3, self.p)
        return b"\1" + self.dump(g2a, g3a)

    def _step_1(self, data):
        pw = self.pw
        g2a, g3a = self.load(data)
        y = self.__secret
        if g2a == 1 or g3a == 1:
            self.abort("condition failed")
        p, g1, a2, a3 = self.p, self.g1, self.a2, self.a3
        b2 = self.b2 = self.__random.randint(1, 2**1536)
        b3 = self.b3 = self.__random.randint(1, 2**1536)
        g2b = pw(g1, b2, p)
        g3b = pw(g1, b3, p)
        g2 = pw(g2a, b2, p)
        g3 = pw(g3a, b3, p)
        r = self.__random.randint(1, 2**1536)
        Pb = self.Pb = pw(g3, r, p)
        Qb = self.Qb = (pw(g1, r, p) * pw(g2, y, p)) % p
        return b"\2" + self.dump(g2b, g3b, Pb, Qb)

    def _step_2(self, data):
        pw = self.pw
        g2b, g3b, Pb, Qb = self.load(data)
        if g2b == 1 or g3b == 1:
            self.abort("condition failed")
        x = self.__secret
        del self.__secret
        p, g1, a2, a3 = self.p, self.g1, self.a2, self.a3
        g2 = pw(g2b, a2, p)
        g3 = pw(g3b, a3, p)
        s = self.__random.randint(1, 2**1536)
        Pa = self.Pa = pw(g3, s, p)
        Qa = self.Qa = (pw(g1, s, p) * pw(g2, x, p)) % p
        del x
        Ra = (pw(Qa, a3, p) * pw(Qb, -a3, p)) % p
        return b"\3" + self.dump(Pa, Qa, Ra)

    def _step_3(self, data):
        pw = self.pw
        Pa, Qa, Ra = self.load(data)
        b3 = self.b3
        Pb, Qb = self.Pb, self.Qb
        p, g1, a2, a3 = self.p, self.g1, self.a2, self.a3
        Rb = (pw(Qa, b3, p) * pw(Qb, -b3, p)) % p
        Rab = pw(Ra, b3, p)
        if Rab != (Pa * pw(Pb, -1, p)) % p:
            self.abort("failed")
        return b"\4" + self.dump(Rb, Pa, Pb)

    def _step_4(self, data):
        pw = self.pw
        Rb, Pa, Pb = self.load(data)
        p, a3 = self.p, self.a3
        Rab = pw(Rb, a3, p)
        if Rab != (Pa * pw(Pb, -1, p)) % p:
            self.abort("failed")

    def abort(self, reason="aborted"):
        raise SocialistMillionaireError(reason)

    def handle(self, message):
        try:
            if message[0] == 255:
                self.abort("abort requested")
            elif message[0] == 1:
                return self._step_1(message[1:])
            elif message[0] == 2:
                return self._step_2(message[1:])
            elif message[0] == 3:
                return self._step_3(message[1:])
            elif message[0] == 4:
                return self._step_4(message[1:])
            elif message == b'':
                self.abort("empty message")
            else:
                self.abort("invalid message ({:d})".format(message[0]))
        except Exception as e:
            self.abort("other error ({:r})".format(e))

help(__name__)

alice = SocialistMillionaire(b"he1llo")
bob = SocialistMillionaire(b"he1llo")

x0 = alice.start()
y0 = bob.start()
print("1/5")

x1 = alice.handle(y0)
y1 = bob.handle(x0)
print("2/5")

x2 = alice.handle(y1)
y2 = bob.handle(x1)
print("3/5")

x3 = alice.handle(y2)
y3 = bob.handle(x2)
print("4/5")

alice.handle(y3)
bob.handle(x3)
print("5/5")






















