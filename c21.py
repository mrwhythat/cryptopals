# ------------------------------------------------------------------------------
# challenge 21
#
# Implement the MT19937 Mersenne Twister RNG
# ------------------------------------------------------------------------------


WIDTH = 32
N, M, R = 624, 397, 31
A = 0x9908B0DF
U, D = 11, 0xFFFFFFFF
S, B = 7, 0x9D2C5680
T, C = 15, 0xEFC60000
L, F = 18, 1812433253
UMASK, LMASK = 0x80000000, 0x7FFFFFFF


class MT19937:
    def __init__(self, seed):
        self.index = N
        self.mt = [seed & 0xFFFFFFFF] + [0 for _ in range(N - 1)]
        for i in range(1, N):
            e = F * (self.mt[i - 1] ^ self.mt[i - 1] >> (WIDTH - 2)) + i
            self.mt[i] = e & 0xFFFFFFFF

    def _temper(self, x):
        x ^= (x >> U) & D
        x ^= (x << S) & B
        x ^= (x << T) & C
        x ^= x >> L
        return x

    def _twist(self):
        for i in range(N - 1):
            y = (self.mt[i] & UMASK) | ((self.mt[i + 1] % N) & LMASK)
            self.mt[i] = self.mt[(i + M) % N] ^ (y >> 1) ^ (A if y & 1 else 0)
        self.index = 0

    def __iter__(self):
        while True:
            if self.index >= N:
                self._twist()
            y = self.mt[self.index]
            self.index += 1
            yield self._temper(y) & 0xFFFFFFFF


# testing
if __name__ == "__main__":
    from itertools import islice
    for n in islice(MT19937(1), 10):
        print(n)
