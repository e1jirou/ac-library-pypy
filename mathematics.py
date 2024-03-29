# divisors(12) = [1,2,3,4,6,12]
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


# prime_factorization(60) = {2:2, 3:1, 5:1}
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


# prime_numbers(n) = [p | (p ∈ prime numbers) and p < n]
# prime_numbers(11) = [2,3,5,7]
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

    def prime_factorization(self, x):
        assert 0 < x < self.n
        res = dict()
        while 1 < x:
            if self.sieve[x] not in res:
                res[self.sieve[x]] = 1
            else:
                res[self.sieve[x]] += 1
            x //= self.sieve[x]
        return res
    
    def divisors(self, x):
        assert 0 < x < self.n
        dic = self.prime_factorization(x)
        res = [1]
        for key, value in dic.items():
            size = len(res)
            res += [0] * (value * size)
            for i in range(value):
                for j in range(size):
                    res[(i + 1) * size + j] = key * res[i * size + j]
        return res


# a*x + b*y = gcd(a,b)
# ext_Euclid(a, b) = gcd(a,b), x, y
def ext_Euclid(a, b):
    if 0 < b:
        gcd_ab, x, y = ext_Euclid(b, a%b)
        return gcd_ab, y, x - (a//b)*y
    return a, 1, 0


# floor_sqrt(n) = floor(sqrt(n))
def floor_sqrt(n):
    # Binary Search
    left = 0
    right = n
    while left < right:
        center = (left + right + 1) // 2
        if center * center <= n:
            left = center
        else:
            right = center - 1
    return left


# dlp_solver(a, b, mod)
# = min(i | a^i ≡ b)
def dlp_solver(a, b, mod):
    # Discrete Logarithm Problem
    # baby-step giant-step
    a %= mod
    b %= mod
    m = floor_sqrt(mod) + 1
    babies = dict()
    pow_a = 1
    for i in range(m):
        if pow_a in babies:
            break
        babies[pow_a] = i
        pow_a = (pow_a * a) % mod
    # inv ≡ 1 / a
    inv = pow(a, mod - 2, mod)
    # r ≡ 1 / a^m
    r = pow(inv, m, mod)
    for i in range(m):
        if b in babies:
            return m * i + babies[b]
        b = b * r % mod
    return -1


# floor_sum(n, m, a, b) = sum([(a*i + b)//m for i in range(n)])
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
