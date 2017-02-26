# ------------------------------------------------------------------------------
# challenge 15
#
# PKCS#7 padding validation
# ------------------------------------------------------------------------------
from c09 import pkcs7_trim


# solution
def pkcs7_check(bs):
    return pkcs7_trim(bs)
