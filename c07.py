# ------------------------------------------------------------------------------
# challenge 07
#
# decrypt AES ECB mode encrypted text
# ------------------------------------------------------------------------------
from base64 import b64decode
from Crypto.Cipher import AES


# solution
def aes_ecb_decrypt(ctext, key):
    blockdata = AES.new(key, AES.MODE_ECB).decrypt(ctext)
    bytesdata = blockdata[:-int(blockdata[-1])]  # padding
    return bytesdata.decode('utf-8')

# testing
if __name__ == "__main__":
    with open('data/7.txt') as f:
        key = 'YELLOW SUBMARINE'
        print(aes_ecb_decrypt(b64decode(f.read()), bytes(key, 'ascii')))
