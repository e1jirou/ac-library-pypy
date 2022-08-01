def comb(n, r):
    r = min(r, n-r)
    res = 1
    for i in range(r):
        res *= n - i
        res //= i + 1
    return res


class Factorials:
    def __init__(self, n, mod):
        self.n = n + 1
        self.mod = mod

        # self.f[i] ≡ i!
        self.f = [1] * self.n
        for i in range(2, self.n):
            self.f[i] = self.f[i-1] * i % mod

        # self.g[i] ≡ 1 / i!
        self.g = [0] * self.n
        self.g[n] = pow(self.f[n], mod-2, mod)
        for i in reversed(range(n)):
            self.g[i] = self.g[i+1] * (i+1) % mod

    # self.fact(n) ≡ n!
    def fact(self, n):
        return self.f[n]

    # self.fact_inv(self, n) ≡ 1 / n!
    def fact_inv(self, n):
        return self.g[n]

    # self.comb(n, r) ≡ nCr ≡ n! / (r! * (n-r)!)
    def comb(self, n, r):
        return self.f[n] * self.g[r] % self.mod * self.g[n-r] % self.mod
    
    # self.perm(n, r) ≡ nPr ≡ n! / (n-r)!
    def perm(self, n, r):
        return self.f[n] * self.g[n-r] % self.mod

    # self.inv(n) ≡ 1 / n ≡ pow(n, mod-2, mod)
    def inv(self, n):
        return self.f[n-1] * self.g[n] % self.mod
