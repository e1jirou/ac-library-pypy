class SegmentTree():
    """
    Reference
    https://github.com/atcoder/ac-library/blob/master/atcoder/segtree.hpp
    https://github.com/atcoder/ac-library/blob/master/document_en/segtree.md
    https://github.com/atcoder/ac-library/blob/master/document_ja/segtree.md
    """
    def __init__(self, n, op, e):
        self.n = n
        self.op = op
        self.e = e
        self.log = (n - 1).bit_length()
        self.size = 1 << self.log
        self.d = [e] * (2 * self.size)

    def update(self, k):
        self.d[k] = self.op(self.d[2*k], self.d[2*k + 1])

    def build(self, v):
        assert len(v) <= self.n
        for i in range(len(v)):
            self.d[self.size + i] = v[i]
        for i in range(self.size - 1, 0, -1):
            self.update(i)

    def set(self, p, x):
        assert 0 <= p < self.n
        p += self.size
        self.d[p] = x
        for i in range(1, self.log+1):
            self.update(p>>i)

    def get(self, p):
        assert 0 <= p < self.n
        return self.d[p + self.size]

    def prod(self, l, r):
        assert 0 <= l <= r <= self.n
        sml = smr = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                sml = self.op(sml, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.op(self.d[r], smr)
            l >>= 1
            r >>= 1
        return self.op(sml, smr)
 
    def all_prod(self):
        return self.d[1]
 
    def max_right(self, l, f):
        assert 0 <= l <= self.n
        assert f(self.e)
        if l == self.n:
            return self.n
        l += self.size
        sm = self.e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not f(self.op(sm, self.d[l])):
                while l < self.size:
                    l = 2 * l
                    if f(self.op(sm, self.d[l])):
                        sm = self.op(sm, self.d[l])
                        l += 1
                return l - self.size
            sm = self.op(sm, self.d[l])
            l += 1
            if (l & -l) == l:
                break
        return self.n
 
    def min_left(self, r, f):
        assert 0 <= r <= self.n
        assert f(self.e)
        if r == 0:
            return 0
        r += self.size
        sm = self.e
        while True:
            r -= 1
            while r > 1 and (r % 2):
                r >>= 1
            if not f(self.op(self.d[r], sm)):
                while r < self.size:
                    r = 2*r + 1
                    if f(self.op(self.d[r], sm)):
                        sm = self.op(self.d[r], sm)
                        r -= 1
                return r + 1 - self.size
            sm = self.op(self.d[r], sm)
            if (r & -r) == r:
                break
        return 0
