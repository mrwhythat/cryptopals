# ------------------------------------------------------------------------------
# challenge 05
#
# implementation of repeating key XOR cipher
# ------------------------------------------------------------------------------
from c02 import bytes_xor


# solution
def rxor_encrypt(s, key):
    """
    Encrypt plain ASCII string with repeating key XOR cipher wiht hex encoding
    """
    return bytes_xor(bytes(s, 'utf-8'), bytes(key, 'utf-8')).hex()


# testing
if __name__ == "__main__":
    s = "Burning 'em, if you ain't quick and nimble\n" \
        "I go crazy when I hear a cymbal"
    key = 'ICE'
    r = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d6' \
        '3343c2a26226324272765272a282b2f20430a652e2c652a3124' \
        '333a653e2b2027630c692b20283165286326302e27282f'
    res = rxor_encrypt(s, key)
    print(res)
    if res == r:
        print('OK')
    else:
        print('test failed')
