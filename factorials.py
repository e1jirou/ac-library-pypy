def comb(n, r):
    r = min(r, n-r)
    res = 1
    for i in range(r):
        res *= n-i
        res //= i+1
    return res


class Factorials:
    def __init__(self, n, mod):
        self.mod = mod

        # self.fac[i] ≡ i!
        self.fac = [1] * (n+1)
        for i in range(2, n+1):
            self.fac[i] = self.fac[i-1] * i % mod

        # self.rec[i] ≡ 1 / i!
        self.rec = [1] * (n+1)
        self.rec[n] = pow(self.fac[n], mod-2, mod)
        for i in range(n-1, 1, -1):
            self.rec[i] = self.rec[i+1] * (i+1) % mod

    # self.comb(n, r) ≡ nCr
    def comb(self, n, r):
        return self.fac[n] * self.rec[r] * self.rec[n-r] % self.mod
    
    # self.perm(n, r) ≡ nPr
    def perm(self, n, r):
        return self.fac[n] * self.rec[n-r] % self.mod

    # self.inv(n) ≡ 1 / n ≡ pow(n, mod-2, mod)
    def inv(self, n):
        return self.fac[n-1] * self.rec[n] % self.mod
