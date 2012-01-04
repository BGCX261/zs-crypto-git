
import os
import hashlib
import random


def oaep_encode(digestmod, message, k, label=b''):
    ''' encode message - k is the length of the rsa modulus in bytes '''
    mgf = make_mgf(digestmod)
    label_hash = digestmod(label).digest()
    length, hash_length = len(message), len(label_hash)
    if length > k - 2 * hash_length - 2:
        raise ValueError("Message too long")
    ps = b'\0' * (k - length - 2 * hash_length - 2)
    db = label_hash + ps + b'\1' + message
    assert len(db) == k - hash_length - 1, "DB length is incorrect"
    seed = os.urandom(hash_length)
    db_mask = mgf(seed, k - hash_length - 1)
    masked_db = bytes(i ^ j for i, j in zip(db, db_mask))
    seed_mask = mgf(masked_db, hash_length)
    masked_seed = bytes(i ^ j for i, j in zip(seed, seed_mask))
    message = b'\0' + masked_seed + masked_db
    return int.from_bytes(message, 'big')

def oaep_decode(digestmod, message, k, label=b''):
    ''' decode message - k is the length of the rsa modulus in bytes '''
    message = message.to_bytes(k, 'big')
    mgf = make_mgf(digestmod)
    label_hash = digestmod(label).digest()
    length, hash_length = len(message), len(label_hash)
    y = message[0]
    masked_seed = message[1:hash_length + 1]
    masked_db = message[hash_length + 1:]
    seed_mask = mgf(masked_db, hash_length)
    seed = bytes(i ^ j for i, j in zip(masked_seed, seed_mask))
    db_mask = mgf(seed, k - hash_length - 1)
    db = bytes(i ^ j for i, j in zip(masked_db, db_mask))
    alleged_label_hash = db[:hash_length]
    i = hash_length
    while i < len(db) and db[i] != 1:
        i += 1
    ps = db[hash_length:i]
    message = db[i + 1:]
    message_invalid = False
    if i == len(db):
        message_invalid = True
    if alleged_label_hash != label_hash:
        message_invalid = True
    if y != 0:
        message_invalid = True
    if message_invalid:
        raise ValueError("decoding error")
    return message
