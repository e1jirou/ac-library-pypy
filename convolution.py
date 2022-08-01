mod = 998244353
"""
Reference
https://github.com/atcoder/ac-library/blob/master/atcoder/convolution.hpp
https://github.com/atcoder/ac-library/blob/master/atcoder/internal_math.hpp
https://github.com/atcoder/ac-library/blob/master/document_en/convolution.md
https://github.com/atcoder/ac-library/blob/master/document_ja/convolution.md
"""

def primitive_root(m):
    if m == 2:
        return 1
    if m == 167772161:
        return 3
    if m == 469762049:
        return 3
    if m == 754974721:
        return 11
    if m == 998244353:
        return 3
    divs = [0] * 20
    divs[0] = 2
    cnt = 1
    x = (m - 1) // 2
    while x % 2 == 0:
        x //= 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            divs[cnt] = i
            cnt += 1
            while x % i == 0:
                x //= i
        i += 2
    if x > 1:
        divs[cnt] = x
        cnt += 1
    g = 2
    while True:
        ok = True
        for i in range(cnt):
            if pow(g, (m - 1) // divs[i], m) == 1:
                ok = False
                break
        if ok:
            return g
        g += 1


class FFT_INFO:
    def __init__(self):
        self.g = primitive_root(mod)
        self.rank2 = ((mod - 1) & (1 - mod)).bit_length() - 1
        self.root = [0] * (self.rank2 + 1)
        self.root[self.rank2] = pow(self.g, (mod - 1) >> self.rank2, mod)
        self.iroot = [0] * (self.rank2 + 1)
        self.iroot[self.rank2] = pow(self.root[self.rank2], mod - 2, mod)
        for i in range(self.rank2 - 1, -1, -1):
            self.root[i] = self.root[i + 1] * self.root[i + 1] % mod
            self.iroot[i] = self.iroot[i + 1] * self.iroot[i + 1] % mod

        self.rate2 = [0] * max(0, self.rank2 - 1)
        self.irate2 = [0] * max(0, self.rank2 - 1)
        prod = 1
        iprod = 1
        for i in range(self.rank2 - 1):
            self.rate2[i] = self.root[i + 2] * prod % mod
            self.irate2[i] = self.iroot[i + 2] * iprod % mod
            prod *= self.iroot[i + 2]
            prod %= mod
            iprod *= self.root[i + 2]
            iprod %= mod

        self.rate3 = [0] * max(0, self.rank2 - 2)
        self.irate3 = [0] * max(0, self.rank2 - 2)
        prod = 1
        iprod = 1
        for i in range(self.rank2 - 2):
            self.rate3[i] = self.root[i + 3] * prod % mod
            self.irate3[i] = self.iroot[i + 3] * iprod % mod
            prod *= self.iroot[i + 3]
            prod %= mod
            iprod *= self.root[i + 3]
            iprod %= mod


info = FFT_INFO()


def butterfly(a):
    n = len(a)
    h = (n - 1).bit_length()

    length = 0
    while length < h:
        if h - length == 1:
            p = 1 << (h - length - 1)
            rot = 1
            for s in range(1 << length):
                offset = s << (h - length)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p] * rot % mod
                    a[i + offset] = (l + r) % mod
                    a[i + offset + p] = (l - r) % mod
                if s + 1 != (1 << length):
                    rot *= info.rate2[(~s & -~s).bit_length() - 1]
                    rot %= mod
            length += 1
        else:
            # 4-base
            p = 1 << (h - length - 2)
            rot = 1
            imag = info.root[2]
            for s in range(1 << length):
                rot2 = rot * rot % mod
                rot3 = rot2 * rot % mod
                offset = s << (h - length)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p] * rot
                    a2 = a[i + offset + 2 * p] * rot2
                    a3 = a[i + offset + 3 * p] * rot3
                    a1na3imag = (a1 - a3) % mod * imag
                    a[i + offset] = (a0 + a2 + a1 + a3) % mod
                    a[i + offset + p] = (a0 + a2 - a1 - a3) % mod
                    a[i + offset + 2 * p] = (a0 - a2 + a1na3imag) % mod
                    a[i + offset + 3 * p] = (a0 - a2 - a1na3imag) % mod
                if s + 1 != (1 << length):
                    rot *= info.rate3[(~s & -~s).bit_length() - 1]
                    rot %= mod
            length += 2


def butterfly_inv(a):
    n = len(a)
    h = (n - 1).bit_length()

    length = h  # a[i, i+(n<<length), i+2*(n>>length), ...] is transformed 
    while length:
        if length == 1:
            p = 1 << (h - length)
            irot = 1
            for s in range(1 << (length - 1)):
                offset = s << (h - length + 1)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p]
                    a[i + offset] = (l + r) % mod
                    a[i + offset + p] = (l - r) * irot % mod
                if s + 1 != (1 << (length - 1)):
                    irot *= info.irate2[(~s & -~s).bit_length() - 1]
                    irot %= mod
            length -= 1
        else:
            # 4-base
            p = 1 << (h - length)
            irot = 1
            iimag = info.iroot[2]
            for s in range(1 << (length - 2)):
                irot2 = irot * irot % mod
                irot3 = irot2 * irot % mod
                offset = s << (h - length + 2)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p]
                    a2 = a[i + offset + 2 * p]
                    a3 = a[i + offset + 3 * p]
                    a2na3iimag = (a2 - a3) * iimag % mod
                    a[i + offset] = (a0 + a1 + a2 + a3) % mod
                    a[i + offset + p] = (a0  - a1 + a2na3iimag) * irot % mod
                    a[i + offset + 2 * p] = (a0 + a1 - a2 - a3) * irot2 % mod
                    a[i + offset + 3 * p] = (a0  - a1 - a2na3iimag) * irot3 % mod
                if s + 1 != (1 << (length - 2)):
                    irot *= info.irate3[(~s & -~s).bit_length() - 1]
                    irot %= mod
            length -= 2


def convolution_naive(a, b):
    n = len(a)
    m = len(b)
    ans = [0] * (n + m - 1)
    if n < m:
        for j in range(m):
            for i in range(n):
                ans[i + j] += a[i] * b[j]
                ans[i + j] %= mod
    else:
        for i in range(n):
            for j in range(m):
                ans[i + j] += a[i] * b[j]
                ans[i + j] %= mod
    return ans


def convolution_fft(a, b):
    a = a.copy()
    b = b.copy()
    n = len(a)
    m = len(b)
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    butterfly(a)
    b += [0] * (z - m)
    butterfly(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= mod
    butterfly_inv(a)
    a = a[:n + m - 1]
    iz = pow(z, mod - 2, mod)
    for i in range(n + m - 1):
        a[i] *= iz
        a[i] %= mod
    return a


def convolution(a, b):
    n = len(a)
    m = len(b)
    if not n or not m:
        return []
    if min(n, m) <= 60:
        return convolution_naive(a, b)
    return convolution_fft(a, b)
