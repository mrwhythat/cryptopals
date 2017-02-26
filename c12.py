# ------------------------------------------------------------------------------
# challenge 12
#
# byte at a time ECB decryption
# ------------------------------------------------------------------------------
from random import randint
from base64 import b64decode

from c09 import pkcs7_trim
from c10 import aes_ecb_encrypt
from c11 import detect_opmode


# solution
# ------------------------------------------------------------------------------
# CBC oracle
# ------------------------------------------------------------------------------
class cbc_emitter:
    BLK_SIZE = 16
    __pad = b64decode(
        b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24g'
        b'c28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFu'
        b'ZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/'
        b'IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    )

    @staticmethod
    def random_bytes(count):
        return bytes([randint(0, 255) for _ in range(count)])

    def __init__(self):
        self.__key = self.random_bytes(self.BLK_SIZE)

    def __call__(self, ptext):
        return aes_ecb_encrypt(ptext + self.__pad, self.__key)
# ------------------------------------------------------------------------------


def _guess_sizes(emitter):
    lc, i = len(emitter(b'')), 1
    while True:
        lr = len(emitter(b'A' * i))
        if lr != lc:
            return lr - lc, lc
        i += 1


def _check_if_ecb(emitter):
    return detect_opmode(emitter) == 'ECB'


def break_ecb(emitter):
    if not _check_if_ecb(emitter):
        raise Exception('non-ECB oracle')
    bsize, strsize = _guess_sizes(emitter)
    known, num = b'', 0
    while True:
        current = bytearray(b'')
        low, high = bsize * num, bsize * (num + 1)
        for i in range(bsize):
            pad = b'A' * (bsize - i - 1)
            pin = pad + known + current
            d = {emitter(pin + bytes([k]))[low:high]: k for k in range(256)}
            val = d.get(emitter(pad)[low:high])
            if val:
                current.append(val)
            else:
                return pkcs7_trim(known + current).decode('utf-8')
        known += current
        num += 1


# testing
if __name__ == "__main__":
    print(break_ecb(cbc_emitter()))
