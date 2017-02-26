# ------------------------------------------------------------------------------
# challenge 09
#
# implement PKCS#7 padding
# ------------------------------------------------------------------------------


# solution
def pkcs7_pad(bs, block):
    pad = block - len(bs) % block
    return bs + bytes([pad]) * pad


def pkcs7_trim(bs):
    last = bs[-1]
    if len(set(bs[-last:])) == 1:
        return bs[:-last]
    else:
        raise Exception('[ERROR]: invalid pkcs#7 padding')


# testing
if __name__ == "__main__":
    print(pkcs7_pad(b'YELLOW SUBMARINE', 20))
    print(pkcs7_pad(b'YELLOW SUBMARINE', 8))
    print(pkcs7_trim(pkcs7_pad(b'YELLOW SUBMARINE', 8)))
