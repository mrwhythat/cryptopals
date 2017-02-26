# ------------------------------------------------------------------------------
# challenge 08
#
# detect AES ECB mode encryption
# ------------------------------------------------------------------------------
# solution
BS = 16  # block size


def is_aes_ecb(bs):
    """Check if any 16-byte block repeats in byte string"""
    return any([bs[i:i + BS] in bs[i + BS:] for i in range(0, len(bs), BS)])


# testing
if __name__ == "__main__":
    with open('data/8.txt') as f:
        for s in f:
            if is_aes_ecb(bytes.fromhex(s.strip())):
                print('found ECB encrypted line:\n', s)
                break
