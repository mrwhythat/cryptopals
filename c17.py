# ------------------------------------------------------------------------------
# challenge 17
#
# The CBC padding oracle
# ------------------------------------------------------------------------------
from random import randint

from c02 import bytes_xor
from c09 import pkcs7_trim
from c10 import aes_cbc_encrypt, aes_cbc_decrypt
from c11 import random_bytes


# solution
BSIZE = 16
TS = [
    b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
]


# ------------------------------------------------------------------------------
# emitter
# ------------------------------------------------------------------------------
class Oracle:

    def __init__(self):
        self.key = random_bytes(BSIZE)
        self.iv = random_bytes(BSIZE)

    def gen_token(self):
        idx = randint(0, len(TS) - 1)
        token = aes_cbc_encrypt(TS[idx], self.key, self.iv)
        return token, self.iv

    def verify_tocken(self, token):
        try:
            aes_cbc_decrypt(token, self.key, self.iv)
            return True
        except Exception:  # means padding error occured
            return False
# ------------------------------------------------------------------------------


def po_attack(oracle):
    token, iv = oracle.gen_token()
    tblocks = [token[i:i + BSIZE] for i in range(0, len(token), BSIZE)]
    prev, curr_block, res = iv, b'', b''
    for block in tblocks:
        for i in range(1, BSIZE + 1):
            prefix = b'\x00' * (BSIZE - i)
            suffix = bytes_xor(curr_block, bytes([i]) * (i - 1))
            for j in range(1 if i == 1 else 0, 256):
                mask = prefix + bytes([j]) + suffix
                bait = bytes_xor(prev, mask)
                if oracle.verify_tocken(bait + block):
                    curr_block = bytes([i ^ j]) + curr_block
                    break
        res += curr_block
        curr_block = b''
        prev = block
    return pkcs7_trim(res)


# testing
if __name__ == "__main__":
    res = po_attack(Oracle())
    print(res)
    if res in TS:
        print("Haxing is suxessful...")
