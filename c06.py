# ------------------------------------------------------------------------------
# challenge 06
#
# break repeating-key XOR
# ------------------------------------------------------------------------------
from base64 import b64decode
from itertools import zip_longest, combinations
from c02 import bytes_xor
from c03 import guess_key


# solution
def hamming_weight(s):
    """Number of '1' in binary representation of a given byte-string"""
    res = 0
    for b in s:
        h = 0
        while b > 0:
            b &= b - 1
            h += 1
        res += h
    return res


def hamming_dist(b1, b2):
    """Number of bits in which two byte strings differ"""
    return hamming_weight(bytes_xor(b1, b2))


def normalized_hamming_dist(s, k):
    blocks = [s[i:i+k] for i in range(0, len(s), k)][:4]
    block_pairs = list(combinations(blocks, 2))
    vs = [hamming_dist(x[0], x[1])/float(k) for x in block_pairs]
    return sum(vs)/len(vs)


def guess_keysize(s):
    return min(range(2, 42), key=lambda x: normalized_hamming_dist(s, x))


def decrypt_file(fname):
    with open(fname) as f:
        s = b64decode(f.read())
        ksize = guess_keysize(s)
        chunks = [s[i:i + ksize] for i in range(0, len(s), ksize)]
        tchunks = list(map(bytes, zip_longest(*chunks, fillvalue=0)))
        key = []
        for chunk in tchunks:
            key.append(guess_key(chunk)[1])
        print(bytes_xor(s, bytes(key)).decode('utf-8'))


# testing
if __name__ == "__main__":
    decrypt_file('data/6.txt')
