''' Advanced Encryption Standard - Block Cipher '''

# Copyright (c) 2011, Stefano Palazzo <stefano.palazzo@gmail.com>
# Copyright (c) 2011, Zeinab Lotfi <zeinab.l.cs@gmail.com>

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


class AES(object):

    # the block size  of AES is always 16
    # bytes, no matter what the key size is.
    block_size = 16

    # lookup talbe for the rijndael s-box
    sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16]

    # lookup talbe for the inverse rijndael s-box
    rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
            0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
            0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54,
            0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
            0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
            0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8,
            0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
            0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
            0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab,
            0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
            0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
            0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
            0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
            0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
            0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d,
            0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
            0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
            0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60,
            0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
            0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
            0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b,
            0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
            0x21, 0x0c, 0x7d]

    # lookup table for r-con (n**2 in rijndaels finite filed GF(2^8)
    rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
            0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97,
            0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72,
            0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
            0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
            0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
            0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
            0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
            0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
            0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
            0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
            0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
            0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
            0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
            0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
            0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
            0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
            0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
            0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
            0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
            0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74,
            0xe8, 0xcb]

    def __init__(self):
        pass

    @staticmethod
    def xor(a, b):
        ''' bitwise xor on equal length bytearrays '''
        return bytearray(i ^ j for i, j in zip(a, b))

    @staticmethod
    def rotate(word):
        ''' rotate a sequence of bytes eight bits to the left '''
        return word[1:] + word[:1]

    def rijndael_key_schedule(self, key):

        def rijndael_key_schedule_core(key_word, rcon_iteration):

            # rotate eight bits to the left:
            key_word = self.rotate(key_word)
            # apply the s-box to all 4 bytes:
            key_word = bytearray(self.sbox[i] for i in key_word)
            # xor the first byte with the rcon value for the current iteration
            key_word[0] = key_word[0] ^ self.rcon[rcon_iteration]

            return key_word

        # define constants for the length of the key
        # and length of the expanded key, n and b:
        if len(key) == 16:
            n, b = 16, 176
        elif len(key) == 24:
            n, b = 24, 208
        elif len(key) == 32:
            n, b = 32, 240
        else:
            raise ValueError("key must be 16, 24 or 32 bytes long")

        # the expanded key has the length b, and it's 
        # first n bytes are the encryption key itself:
        expanded_key = bytearray(b)
        expanded_key[:len(key)] = key

        current_size = len(key)
        rcon_iteration = 1

        while current_size < b:
            # adding 4 bytes to the expanded key, starting
            # with the value of the previous 4 bytes in the
            # expanded key:

            # expanded_key is the expanded key, cs is the current size of it

            # t is the previous 4 bytes in the expanded key:
            t = expanded_key[current_size - 4:current_size]  #1
            
            # perform the key schedule core on t:
            t = rijndael_key_schedule_core(t, rcon_iteration)
            rcon_iteration += 1
            # exclusive-or t with the 4 bytes before the expanded key
            # and make that the next 4 bytes of the expanded key:
            expanded_key[current_size:current_size + 4] = self.xor(
                expanded_key[current_size - n:current_size - n + 4], t) #2
            current_size += 4

            for i in range(3):
                t = expanded_key[current_size - 4:current_size]  #1
                expanded_key[current_size:current_size + 4] = self.xor(
                    expanded_key[current_size - n:current_size - n + 4], t)  #2
                current_size += 4

            if n == 32:  # if we're generating a 256 bit key
                t = expanded_key[current_size - 4:current_size]  #1
                # run each of the 4 bytes through the rijdael s-box:
                t = bytearray(self.sbox[i] for i in t)
                expanded_key[current_size:current_size + 4] = self.xor(
                    expanded_key[current_size - n:current_size - n + 4], t)  #2
                current_size += 4

            # if we're generating a 128 bit key, don't do the next step,
            # do it 2 times for a 192 bit key, 3 times for a 256 bit key:
            for i in range(0 if n == 16 else 2 if n == 24 else 3):
                t = expanded_key[current_size - 4:current_size]  #1
                expanded_key[current_size:current_size + 4] = self.xor(
                    expanded_key[current_size - n:current_size - n + 4], t)  #2
                current_size += 4

        # because of the last step, the expanded key might be too long:
        return expanded_key[:b]

    def encrypt(self, data, key):
        # determine the number of rounds and raise
        # an exception for wrongly sized keys:
        if len(key) == 16:
            n_rounds = 10
        elif len(key) == 24:
            n_rounds = 12
        elif len(key) == 32:
            n_rounds = 14
        else:
            raise ValueError("key must be 16, 24 or 32 bytes long")
        # empty bytearrays for our current block and the result,
        # bytearrays are the mutable version of <type 'bytes'>:
        block, result = bytearray(16), bytearray(16)

        # get the expanded key from the rijndael key schedule:
        expanded_key = self.rijndael_key_schedule(key)

        # aes operates on a 4 by 4 matrix, the state, which is
        # stored as a flat array in column-major order, such that
        # [[1, 2, 3], [4, 5, 6]] becomes [1, 4, 2, 5, 3, 6]:
        for i in range(4):
            for j in range(4):
                block[(i + (j * 4))] = data[(i * 4) + j]

        # initial round and start of the aes process:
        block = self.main(block, expanded_key, n_rounds)

        # here we turn the flat matrix back into a linear array
        # from column-major order:
        for k in range(4):
            for l in range(4):
                result[(k * 4) + l] = block[(k + (l * 4))]

        # return the result as an immutable bytes object:
        return bytes(result)

    def get_round_key(self, expanded_key, kp):
        round_key = bytearray(16)
        for i in range(4):
            for j in range(4):
                round_key[j * 4 + i] = expanded_key[kp + i * 4 + j]
        return round_key

    def add_round_key(self, state, expanded_key, kp):
        # xor the state with the round key
        return self.xor(state, self.get_round_key(expanded_key, kp))

    def main(self, state, expanded_key, n_rounds):
        # initial round:
        state = self.add_round_key(state, expanded_key, 0)

        # normal rounds:
        for i in range(1, n_rounds - 0):
            print(i)
            state = self.sub_bytes(state)
            print("sub bytes:     ", list(state))
            state = self.shift_rows(state)
            print("shift rows:    ", list(state))
            state = self.mix_columns(state)
            print("mix columns:   ", list(state))
            state = self.add_round_key(state, expanded_key, 16 * i)
            print("add round key: ", list(state))

        # final round
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, expanded_key, 16 * n_rounds)

        return state

    def sub_bytes(self, state):
        return bytearray(self.sbox[i] for i in state)

    def shift_rows(self, state):
        # transform our column-major order array back into a matrix:
        matrix = [bytearray(4) for i in range(4)]
        for i in range(4):
            for j in range(4):
                matrix[i][j] = state[(i * 4) + j]

        # each byte of the nth row is shifted n to the left (0, 1, 2, 3):
        matrix[1] = matrix[1][1:] + matrix[1][:1]
        matrix[2] = matrix[2][2:] + matrix[2][:2]
        matrix[3] = matrix[3][3:] + matrix[3][:3]

        # transform the matrix back to column-major order:
        state = bytearray(16)
        for i in range(4):
            for j in range(4):
                state[(i + (j * 4))] = matrix[j][i]

        return state

    @staticmethod
    def galois_multiplication(a, b):
        ''' remove this: stolen from slowaes '''
        p = 0
        for counter in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            a &= 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p


    def mix_columns(self, state):

        def mix_column(column):
            m = [2, 1, 1, 3]
            
            c = bytearray(i for i in column)
            g = self.galois_multiplication

            column[0] = (g(c[0], m[0]) ^ g(c[3], m[1]) ^
                g(c[2], m[2]) ^ g(c[1], m[3]))
            column[1] = (g(c[1], m[0]) ^ g(c[0], m[1]) ^
                g(c[3], m[2]) ^ g(c[2], m[3]))
            column[2] = (g(c[2], m[0]) ^ g(c[1], m[1]) ^
                g(c[0], m[2]) ^ g(c[3], m[3]))
            column[3] = (g(c[3], m[0]) ^ g(c[2], m[1]) ^
                g(c[1], m[2]) ^ g(c[0], m[3]))

            return column

        for i in range(4):
            # get a column out of our column-major order matrix:
            column = state[i:i + 16:4]
            # apply mix_column to that:
            column = mix_column(column)
            # re-insert the result into the matrix array:
            state[i:i + 16:4] = column
        return state


def test_key_schedule():

    a = AES()

    assert a.rijndael_key_schedule(b"\1" * 16) == bytearray(b"\x01\x01\x01"
        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01|}}}}||||}}}}"
        b"|||nmm\x82\x13\x11\x11\xfeoll\x83\x12\x10\x10\xff\xa0\xa7{K\xb3\xb6"
        b"j\xb5\xdc\xda\x066\xce\xca\x16\xc9\xdc\xe0\xa6\xc0oV\xccu\xb3\x8c"
        b"\xcaC}F\xdc\x8a\x96f\xd8?\xf90\x14JJ\xbc\xde\t7\xfa\x02\x83\x9b\x11"
        b"4\xa5b! \xef(\x9d\xfe\xe6\x1fg\xfce^\xa1ye<\x80Y\x8a\x14\x1d\xa7l"
        b"\x0bz[\t\x04\x98xN8\x18!\xc4,\x05\x86\xa8\'\x7f\xdd\xa1\xcdYJ\x82"
        b"\xf5AkF\xd9D\xed\xee\xfe;0O\x19]\xce9\xec\x1c\xa5\x7f5XH\x91\xcb"
        b"cx\xde")

    assert a.rijndael_key_schedule(b"\1" * 24) == bytearray(b"\x01\x01\x01"
        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
        b"\x01\x01\x01\x01\x01|}}}}||||}}}}||||}}}}|||nmm\x82\x13\x11\x11"
        b"\xfeoll\x83\x12\x10\x10\xffnmm\x82\x13\x11\x11\xfe\xe8\xef\xd6\xff"
        b"\xfb\xfe\xc7\x01\x94\x92\xab\x82\x86\x82\xbb}\xe8\xef\xd6\xff\xfb"
        b"\xfe\xc7\x01[)\xaa\xf0\xa0\xd7m\xf14E\xc6s\xb2\xc7}\x0eZ(\xab\xf1"
        b"\xa1\xd6l\xf0\xbdy&\xc2\x1d\xaeK3)\xeb\x8d@\x9b,\xf0N\xc1\x04[\xbf"
        b"`\xd27O(\xe3\xa2\x125M\xe9!\x1c\xa6da\x87\x8a\x94/F\x8e\xcf\x90&\\"
        b"\xf8\xdf\"\xa2<\xe5\x17\xef\xd5\xc4\x0bI\xb1\xa5\x8c\xc3%\x8a\xcaM"
        b"\xea\x1a\xec\x11\x12\xc5 k\x9a+7\x84O\xef<\xcd\xfeJ\xb0\x0e\xdb\xc0")

    assert a.rijndael_key_schedule(b"\1" * 32) == bytearray(b"\x01\x01\x01"
        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01|}}}}||||}}}}"
        b"|||\xfe\x11\x11\x11\xff\x10\x10\x10\xfe\x11\x11\x11\xff\x10\x10"
        b"\x10\xb4\xb7\xb7k\xc9\xcb\xcb\x17\xb5\xb6\xb6j\xc8\xca\xca\x16\x16"
        b"eeV\xe9uuF\x17ddW\xe8ttG\"%\x17\xf0\xeb\xee\xdc\xe7^Xj\x8d\x96\x92"
        b"\xa0\x9b\x86*\x85Bo_\xf0\x04x;\x94S\x90O\xe0\x14\xae\xc4\xed\x90E*"
        b"1w\x1br[\xfa\x8d\xe0\xfba\xdb\xcb\x8a\xad\xb4\x94z\xa9\xcc\xaf\xee"
        b"\xfa\\\xe0\x0e\xee_o\xc5\xda\x1aE\xf4\xad\x017\xafW\x8c\xd7T6\xbf"
        b"\xc5\xaa\xa8\x0bQ\xd0\x01\xc7\xfe>\xfb\x9b\x1e0\x15\rk\x9c\xce\x17"
        b".hc\x16\x19\xc74\x9a\xce\x93\x02\x07Nv\xdf\x0c\x1f\xa6\xde\xcb\xe1"
        b"\x98%P\xff\xa80[\xa9\x98\x9dL\x87\xf0\xfeZ\x9e7\xca\xc0P\xa4\xc8")

    print("key schedule: all tests passed")

def test_shift_rows():
    a = AES()
    assert a.shift_rows(bytearray(range(1, 17))) == bytearray(
        [1, 2, 3, 4, 6, 7, 8, 5, 11, 12, 9, 10, 16, 13, 14, 15])
    print("shift rows: all tests passed")


def test_shift_rows():
    a = AES()
    assert a.shift_rows(bytearray(range(1, 17))) == bytearray(
        [1, 2, 3, 4, 6, 7, 8, 5, 11, 12, 9, 10, 16, 13, 14, 15])
    print("shift rows: all tests passed")


def test_mix_columns():
    a = AES()
    assert a.mix_columns(bytearray(range(1, 17))) == bytearray(
        [9, 10, 11, 12, 29, 30, 31, 16, 1, 2, 3, 36, 21, 22, 23, 40])
    print("mix_columns: all tests passed")


def test_encryption():
    a = AES()
    print(a.encrypt(b"d" * 16, b"k" * 32))
    print(b'\xa7i\xfdW\x98T@{v\xdd\x05Ye\x87I\xb7')
    assert a.encrypt(b"d" * 16, b"k" * 32) == b'\xa7i\xfdW\x98T@{v\xdd\x05Ye\x87I\xb7'
    print("encryption: all tests passed")


if __name__ == '__main__':
    test_key_schedule()
    test_shift_rows()
    test_mix_columns()

    test_encryption()
