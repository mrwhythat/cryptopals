# ------------------------------------------------------------------------------
# challenge 14
#
# byte-at-a-time ECB decryption (Harder)
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
        self.__prefix = self.random_bytes(randint(0, 30))
        self.__key = self.random_bytes(self.BLK_SIZE)

    def __call__(self, ptext):
        return aes_ecb_encrypt(self.__prefix + ptext + self.__pad, self.__key)
# ------------------------------------------------------------------------------


def _guess_sizes(emitter):
    # get block size
    p = b''
    olen = len(emitter(p))
    while True:
        p += b'A'
        lr = len(emitter(p))
        if lr != olen:
            bsize = lr - olen
            break

    # get ending block for prefix
    orig, padded = emitter(b''), emitter(b'A')
    orig_bs = [orig[i:i + bsize] for i in range(0, len(orig), bsize)]
    padded_bs = [padded[i:i + bsize] for i in range(0, len(padded), bsize)]
    i = 0
    while orig_bs[i] == padded_bs[i]:
        i += 1
    start, end = i * bsize, (i + 1) * bsize

    # get ending position in block for prefix
    j, prev, new = 1, orig_bs[i], emitter(b'A')[start:end]
    while new != prev:
        j += 1
        prev, new = new, emitter(b'A' * j)[start:end]
    padsize = j - 1

    return bsize, i, padsize


def _check_if_ecb(emitter):
    return detect_opmode(emitter) == 'ECB'


def break_ecb(emitter):
    if not _check_if_ecb(emitter):
        raise Exception('non-ECB oracle')
    bsize, blocknum, padsize = _guess_sizes(emitter)
    known, num = b'', blocknum + 1
    while True:
        current = bytearray(b'')
        low, high = bsize * num, bsize * (num + 1)
        for i in range(bsize):
            pad = b'A' * (padsize + bsize - i - 1)
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
