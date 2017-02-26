# ------------------------------------------------------------------------------
# challenge 02
#
# bitwise XOR of two hex ecoded byte-arrays
# ------------------------------------------------------------------------------


# solution
def expand_bytes(bs, size):
    l = len(bs)
    if l == 0:
        return bs
    d, m = divmod(size, l)
    return bs * d + bs[:m]


def bytes_xor(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, expand_bytes(b2, len(b1)))])


def hex_xor(s1, s2):
    return bytes_xor(bytes.fromhex(s1), bytes.fromhex(s2)).hex()


# testing
if __name__ == "__main__":
    s1 = '1c0111001f010100061a024b53535009181c'
    s2 = '686974207468652062756c6c277320657965'
    r = '746865206b696420646f6e277420706c6179'
    res = hex_xor(s1, s2)
    print(res)
    if res == r:
        print('OK')
    else:
        print('test failed')
    print('by the way, ', end=' ')
    print(bytes.fromhex(s2).decode('utf-8'))
    print(bytes.fromhex(r).decode('utf-8'))
