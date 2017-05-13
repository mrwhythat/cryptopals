# ------------------------------------------------------------------------------
# challenge 10
#
# CBC mode implementation
# ------------------------------------------------------------------------------
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from c02 import bytes_xor
from c09 import pkcs7_pad, pkcs7_trim


# solution
BLK_SIZE = 16


def _aes_ecb_encrypt(ptext, key):
    '''encrypt one block in ecb mode'''
    e = Cipher(algorithms.AES(key), modes.ECB(), default_backend()).encryptor()
    return e.update(ptext) + e.finalize()


def _aes_ecb_decrypt(ctext, key):
    '''decrypt one block in ecb mode'''
    d = Cipher(algorithms.AES(key), modes.ECB(), default_backend()).decryptor()
    return d.update(ctext) + d.finalize()


def aes_ecb_encrypt(ptext, key):
    return _aes_ecb_encrypt(pkcs7_pad(ptext, BLK_SIZE), key)


def aes_ecb_decrypt(ctext, key):
    return pkcs7_trim(_aes_ecb_decrypt(ctext, key))


def aes_cbc_encrypt(ptext, key, iv):
    res, current, padded = b'', iv, pkcs7_pad(ptext, BLK_SIZE)
    for p in [padded[i:i + BLK_SIZE] for i in range(0, len(padded), BLK_SIZE)]:
        current = _aes_ecb_encrypt(bytes_xor(current, p), key)
        res += current
    return res


def aes_cbc_decrypt(ctext, key, iv):
    res, current = b'', iv
    for c in [ctext[i:i + BLK_SIZE] for i in range(0, len(ctext), BLK_SIZE)]:
        res += bytes_xor(_aes_ecb_decrypt(c, key), current)
        current = c
    return pkcs7_trim(res)


# testing
if __name__ == "__main__":
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * BLK_SIZE
    v = b'AAAAAAAAAAAAAAA'
    print(aes_ecb_encrypt(v + b'\x00', key).hex())
    print(aes_ecb_encrypt(v + b'\x01', key).hex())
