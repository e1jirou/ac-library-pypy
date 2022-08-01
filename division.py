# divisors(12) == [1,2,3,4,6,12]
# O(sqrt(n))
def divisors(n):
    assert 0 < n
    res = []
    d = 1
    while d * d < n:
        if n % d == 0:
            res.append(d)
            res.append(n // d)
        d += 1
    if d * d == n:
        res.append(d)
    res.sort()
    return res


# prime_factorization(60) == {2:2, 3:1, 5:1}
# O(sqrt(n))
def prime_factorization(n):
    assert 0 < n
    res = dict()
    p = 2
    while p * p <= n:
        if n % p == 0:
            cnt = 0
            while n % p == 0:
                cnt += 1
                n //= p
            res[p] = cnt
        p += 1
    if 1 < n:
        res[n] = 1
    return res


# prime_numbers(n) == [p | (p ∈ prime numbers) and p < n]
# prime_numbers(11) == [2,3,5,7]
def prime_numbers(n):
    if n <= 2:
        return []
    res = [2]
    for i in range(3, n, 2):
        for p in res:
            if i % p == 0:
                break
            if i < p * p:
                res.append(i)
                break
    return res


class Eratosthenes:
    def __init__(self, n):
        self.n = n
        self.sieve = [0] * n
        self.prime = [2]
        for i in range(2, n, 2):
            self.sieve[i] = 2
        for i in range(3, n, 2):
            for p in self.prime:
                if i % p == 0:
                    self.sieve[i] = p
                    break
                if i < p * p:
                    self.sieve[i] = i
                    self.prime.append(i)
                    break

    def prime_factorization(self, n):
        assert 0 < n < self.n
        res = dict()
        while 1 < n:
            if self.sieve[n] not in res:
                res[self.sieve[n]] = 1
            else:
                res[self.sieve[n]] += 1
            n //= self.sieve[n]
        return res


# a*x + b*y == gcd(a,b)
# ext_Euclid(a, b) == gcd(a,b), x, y
def ext_Euclid(a, b):
    if 0 < b:
        gcd_ab, x, y = ext_Euclid(b, a%b)
        return gcd_ab, y, x - (a//b)*y
    return a, 1, 0


# floor_sum(n, m, a, b) == sum([(a*i + b)//m for i in range(n)])
def floor_sum(n, m, a, b):
    assert 0 <= n
    assert 1 <= m
    ans = 0
    while True:
        ans += (a//m * n * (n-1))//2 + b//m * n
        a %= m
        b %= m
        if a*n + b < m:
            return ans
        new_n = (a*n + b) // m
        max_x = -(b - m*new_n) // a
        ans += (n - max_x) * new_n
        n, m, a, b = new_n, a, m, a*max_x - m*new_n + b
