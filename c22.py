# ------------------------------------------------------------------------------
# challenge 22
#
# Break MT19937 seed
# ------------------------------------------------------------------------------

import time
import random

from c21 import MT19937


# implementation
def generator():
    '''Seed MT19937 PRNG with unknown timestamp, return first output'''
    bsleep = random.randint(40, 500)
    time.sleep(bsleep)
    mt = MT19937(int(time.time()))
    asleep = random.randint(40, 500)
    time.sleep(asleep)
    return next(iter(mt))


def crack_generator(output):
    '''Crack time-seeded MT19937 PRNG by its first output'''
    for i in range(int(time.time()), 0, -1):
        if next(iter(MT19937(int(i)))) == output:
            print("secret seed is: {}".format(i))
            break


# testing
if __name__ == "__main__":
    crack_generator(generator())
