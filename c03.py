# ------------------------------------------------------------------------------
# challenge 03
#
# decode string XORed with single character, using English language metrics
# ------------------------------------------------------------------------------
from c02 import bytes_xor


# solution
freqs = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835,
    'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610, 'h': 0.0492888,
    'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
    'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302, 'p': 0.0137645,
    'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357,
    'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
    'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}


def englishness(s):
    """Compute a number of likeliness for a string to be English"""
    def score(c):
        lc = c.lower()
        return freqs[lc] if lc in freqs else 0
    return sum(map(score, s))


def guess_key(bs):
    variants = []
    for i in range(128):
        variants.append((bytes_xor(bs, bytes([i])).decode('utf-8'), i))
    return max(variants, key=lambda x: englishness(x[0]))


def break_mtp(s):
    bs = bytes.fromhex(s)
    variants = [bytes_xor(bs, bytes([i])).decode('utf-8') for i in range(128)]
    return max(variants, key=englishness)


# testing
if __name__ == "__main__":
    x = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print(break_mtp(x))
