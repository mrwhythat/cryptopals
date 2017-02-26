# ------------------------------------------------------------------------------
# challenge 20
#
# Break fixed-nonce CTR statistically
# ------------------------------------------------------------------------------
import os
from base64 import b64decode

from c02 import bytes_xor as xor
from c03 import englishness
from c18 import BSIZE, aes_ctr_encrypt as encrypt


# solution
def prepare_data():
    key, nonce = os.urandom(BSIZE), 0
    with open('data/20.txt') as f:
        data = map(lambda x: encrypt(b64decode(x), key, nonce), f.readlines())
        return list(data)


def break_fixed_nonce_ctx(pieces):
    # copy that data to local list
    data = list(pieces)
    # create buffer for key bytes
    key_bytes = []
    start = 0
    # until all available ciphertext are not completely decoded
    while data:
        # find minimal ciphertext length
        shortest = min(enumerate(data), key=lambda x: len(x[1]))
        end = len(shortest[1])
        # transposed samples
        samples = list(zip(*(ct[start:end] for ct in data)))
        # for each byte of 'key'
        for i in range(start, end):
            # test for the frequencies at the beginning of the line
            def eng_test(x):
                return englishness(x[0], len(data) == len(pieces) and i == 0)
            # select key byte that maximises 'englishness' of the byte view
            vs = []
            for k in range(256):
                vs.append((xor(samples[i - start], bytes([k]) * len(data)), k))
            variant = max(vs, key=eng_test)
            key_bytes.append(variant[1])
        del data[shortest[0]]
        start = end
    # decode data with the computed key
    return list(xor(ct[:end], bytes(key_bytes)[:end]) for ct in pieces)


if __name__ == '__main__':
    decoded = break_fixed_nonce_ctx(prepare_data())
    print(b'\n'.join(decoded).decode('utf-8'))
