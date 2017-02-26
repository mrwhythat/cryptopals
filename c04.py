# ------------------------------------------------------------------------------
# challenge 04
#
# detect single-byte encoded string in a file
# ------------------------------------------------------------------------------
from c02 import bytes_xor
from c03 import englishness


# solution
def string_englishness(s):
    bs = bytes.fromhex(s)
    best_val, max_eng = '', 0
    for i in range(128):
        try:
            val = bytes_xor(bs, bytes([i])).decode('utf-8')
            eng = englishness(val)
            if max_eng < eng:
                best_val, max_eng = val, eng
        except:
            continue
    return (max_eng, best_val)


def detect_encoded(fname):
    with open(fname) as f:
        return max([string_englishness(l.strip()) for l in f.readlines()])[1]


# testing
if __name__ == "__main__":
    print(detect_encoded('data/4.txt'))
