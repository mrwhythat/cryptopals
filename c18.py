# ------------------------------------------------------------------------------
# challenge 18
#
# Implement CTR, the stream cipher mode
# ------------------------------------------------------------------------------
import struct
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from c02 import bytes_xor


# solution
BSIZE = 16


class KeyStreamEndException(Exception):
    pass


def aes_ctr_encrypt(ptext, key, nonce):
    return _keystream_xor(ctext, key, nonce)


def aes_ctr_decrypt(ctext, key, nonce):
    return _keystream_xor(ctext, key, nonce)


def _keystream_xor(data, key, nonce):
    res = b''
    for pad, chunk in zip(
            _keystream(key, nonce),
            [data[i:i + BSIZE] for i in range(0, len(data), BSIZE)]
    ):
        res += bytes_xor(chunk, pad)
    return res


def _keystream(key, nonce):
    c = Cipher(algorithms.AES(key), modes.ECB(), default_backend()).encryptor()
    nonce_bytes = struct.pack('<Q', nonce)
    for count in range(2 ** 64 - 1):
        count_bytes = struct.pack('<Q', count)
        block = nonce_bytes + count_bytes
        yield c.update(block)
    raise KeyStreamEndException()

# testing
if __name__ == "__main__":
    string = base64.b64decode(
        'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/'
        '2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    )
    key = b'YELLOW SUBMARINE'
    print(aes_ctr_decrypt(string, key, 0))
