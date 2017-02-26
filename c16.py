# ------------------------------------------------------------------------------
# challenge 16
#
# CBC bitflipping attacks
# ------------------------------------------------------------------------------
from urllib.parse import quote_plus

from c02 import bytes_xor
from c10 import aes_cbc_encrypt, aes_cbc_decrypt
from c11 import random_bytes


# solution
BSIZE = 16
PREFIX = b'comment1=cooking%20MCs;userdata='
SUFFIX = b';comment2=%20like%20a%20pound%20of%20bacon'


# ------------------------------------------------------------------------------
# emitter
# ------------------------------------------------------------------------------
class Oracle:
    def __init__(self):
        self.key, self.iv = random_bytes(BSIZE), random_bytes(BSIZE)

    def encrypt(self, v):
        return aes_cbc_encrypt(
            PREFIX + bytes(quote_plus(v), 'ascii') + SUFFIX,
            self.key,
            self.iv
        )

    def decrypt(self, s):
        return {k: v for k, v in map(
            lambda x: x.split(b'='),
            aes_cbc_decrypt(s, self.key, self.iv).split(b';')
        )}.get(b'admin', False)
# ------------------------------------------------------------------------------


def bitflip_attack(oracle):
    target = b';admin=true;c=mo'
    ct = oracle.encrypt(b'')
    ct_blocks = [ct[i:i + BSIZE] for i in range(0, len(ct), BSIZE)]
    c1 = ct_blocks[1]
    m2 = SUFFIX[:BSIZE]
    pad = bytes_xor(c1, m2)
    bait = bytes_xor(target, pad)
    payload = b''.join([ct_blocks[0], bait] + ct_blocks[2:])
    return oracle.decrypt(payload)


# testing
if __name__ == "__main__":
    if bitflip_attack(Oracle()):
        print('Haxing iz suxessful!')
