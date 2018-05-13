# ------------------------------------------------------------------------------
# challenge 23
#
# Clone an MT19937 RNG from its output
# ------------------------------------------------------------------------------

from itertools import islice

from c21 import MT19937, U, S, B, T, C, L, N


class MT19937Adversary(MT19937):
    def __init__(self, target):
        """
        Wrap initialization with splicing of first N inverted outputs
        """
        super().__init__(1)
        for i, x in enumerate(islice(target, N)):
            self.mt[i] = self._untemper(x)

    def _untemper(self, x):
        """
        Invert tempering operation of the MT19937 implementation,
        where temper() function is defined as follows:

        op_r(x, r) = x ^ (x >> r); r = 5

        op_l(x, l1, l2) = x ^ ((x << l1) & l2); l1 = 5, l2 = 6581

        """
        x = self._inv_r(x, L)
        x = self._inv_l(x, T, C)
        x = self._inv_l(x, S, B)
        x = self._inv_r(x, U)
        return x

    def _inv_r(self, x, r):
        """
        inv_r(op_r(x, 5), 5):
                      x0: 10110|10001|01011|0
            x1 = x0 >> R: 00000|10110|10001|0
            x2 = x0 ^ x1: 10110|00111|11010|0
            x3 = x2 >> R: 00000|10110|00111|1
            x4 = x2 ^ x3: 10110|10001|11101|1
                          ...
        """
        res = x
        for i in range(32 // r + 1):
            res = x ^ (res >> r)
        return res

    def _inv_l(self, x, l1, l2):
        """
        inv_l(op_l(x, 5, 6581), 5, 6581):
                       x0: 1|01101|00010|10110
            x1 = x0 << L1: 1|00010|10110|00000
                       L2: 0|00110|01101|10101
             x2 = x1 & L2: 0|00010|00100|00000
             x3 = x0 ^ x2: 1|01111|00110|10110
            x4 = x3 << L1: 1|00110|10110|00000
                       L2: 0|00110|01101|10101
             x5 = x4 & L2: 0|00010|00100|00000
             x6 = x3 ^ x5: 1|01101|00010|10110
                           ...
        """
        res = x
        for i in range(32 // l1 + 1):
            res = x ^ ((res << l1) & l2)
        return res


# testing
def test():
    mt = MT19937(5)
    mt_adv = MT19937Adversary(mt)
    for a, b in zip(islice(mt, 10), islice(mt_adv, 10)):
        print("A: {}\nB: {}\n{}".format(a, b, a == b))


if __name__ == "__main__":
    test()
