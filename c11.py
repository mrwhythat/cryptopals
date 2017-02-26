# ------------------------------------------------------------------------------
# challenge 11
#
# CBC/ECB detection oracle
# ------------------------------------------------------------------------------
from random import randint

import c10 as c
from c08 import is_aes_ecb

# solution
BLK_SIZE = 16


def random_bytes(count):
    return bytes([randint(0, 255) for _ in range(count)])


def emit_ctext(ptext):
    padsize = randint(5, 10)
    text = random_bytes(padsize) + ptext + random_bytes(padsize)
    key = random_bytes(BLK_SIZE)
    if randint(0, 1) == 0:
        print('[encrypting in CBC mode]')
        return c.aes_cbc_encrypt(text, key, random_bytes(BLK_SIZE))
    else:
        print('[encrypting in ECB mode]')
        return c.aes_ecb_encrypt(text, key)


def _ecb_test():
    tdata, blob = b'', b'\x00' * BLK_SIZE
    for i in range(BLK_SIZE):
        tdata += b'\x00' * (BLK_SIZE - i) + blob * 2
    return tdata


def detect_opmode(emitter):
    # test ECB
    if is_aes_ecb(emitter(_ecb_test())):
        return 'ECB'
    else:
        return 'CBC'


# testing
if __name__ == "__main__":
    print('{} detected'.format(detect_opmode(emit_ctext)))
