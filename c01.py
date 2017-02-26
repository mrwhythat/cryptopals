# ------------------------------------------------------------------------------
# challenge 01
#
# convert hex encoded string to base64
# ------------------------------------------------------------------------------
import base64


# solution
def hex_to_base64(hexstr):
    return base64.b64encode(bytes.fromhex(hexstr)).decode('utf-8')


# testing
if __name__ == "__main__":
    h = '49276d206b696c6c696e6720796f757220627261696e206c' \
        '696b65206120706f69736f6e6f7573206d757368726f6f6d'
    r = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    res = hex_to_base64(h)
    print(res)
    if res == r:
        print('OK')
    else:
        print('test failed')
