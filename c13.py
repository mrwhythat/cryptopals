# ------------------------------------------------------------------------------
# challenge 13
#
# ECB cut-and-paste
# ------------------------------------------------------------------------------
from random import randint

from c09 import pkcs7_pad
from c10 import aes_ecb_encrypt as _enc, aes_ecb_decrypt as _dec


# solution
def _rand_bytes(n):
    return bytes([randint(0, 255) for _ in range(n)])


def _kv_decode(s):
    return {k: v for k, v in map(lambda x: x.split(b'='), s.split(b'&'))}


def _kv_encode(m):
    return b'&'.join(map(lambda x: b'='.join(x), m))


def _profile_for(m):
    if b'&' in m or b'=' in m:
        raise Exception('invalid character')
    return _kv_encode([[b'email', m], [b'uid', b'10'], [b'role', b'user']])


# ------------------------------------------------------------------------------
# oracle
# ------------------------------------------------------------------------------
class oracle:
    def __init__(self):
        self._key = _rand_bytes(16)

    def dec(self, s):
        return _kv_decode(_dec(s, self._key))

    def enc(self, m):
        return _enc(_profile_for(m), self._key)
# ------------------------------------------------------------------------------


def substitute(oracle):
    bs = 16
    payload = b'hey@there.' + pkcs7_pad(b'admin', bs) + b'com'
    val = oracle.enc(payload)
    admin_block = val[bs:2 * bs]
    forged = val[:bs] + val[2 * bs:3 * bs] + admin_block
    print(oracle.dec(forged))


# testing
if __name__ == "__main__":
    substitute(oracle())
