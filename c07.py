# ------------------------------------------------------------------------------
# challenge 07
#
# decrypt AES ECB mode encrypted text
# ------------------------------------------------------------------------------
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend as backend


# solution
def aes_ecb_decrypt(ctext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend()).decryptor()
    blockdata = cipher.update(ctext) + cipher.finalize()
    bytesdata = blockdata[:-int(blockdata[-1])]  # padding
    return bytesdata.decode('utf-8')

# testing
if __name__ == "__main__":
    with open('data/7.txt') as f:
        key = 'YELLOW SUBMARINE'
        print(aes_ecb_decrypt(b64decode(f.read()), bytes(key, 'ascii')))
