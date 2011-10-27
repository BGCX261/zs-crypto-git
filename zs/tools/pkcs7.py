''' PKCS7 Padding for Block Cipher Modes '''

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


def pad(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    return data + bytes(padding_length for i in range(padding_length))

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

def check_padding(data, block_size):
    if not data or len(data) % block_size:
        raise ValueError("padding error")
    if data[-1] > block_size:
        raise ValueError("padding error")
    if not all(i == data[-1] for i in data[-data[-1]:]):
        raise ValueError("padding error")


def test():
    print("pkcs7: no test implemented")
