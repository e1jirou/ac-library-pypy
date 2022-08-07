class FenwickTree:
    """
    Reference
    https://github.com/atcoder/ac-library/blob/master/atcoder/fenwicktree.hpp
    https://github.com/atcoder/ac-library/blob/master/document_en/fenwicktree.md
    https://github.com/atcoder/ac-library/blob/master/document_ja/fenwicktree.md
    """
    def __init__(self, n):
        # data is 1-indexed
        self.n = n
        self.data = [0] * (n + 1)

    def add(self, p, x):
        assert 0 <= p < self.n
        p += 1
        while p <= self.n:
            self.data[p] += x
            p += p & -p

    def sum_left(self, r):
        s = 0
        while r > 0:
            s += self.data[r]
            r -= r & -r
        return s

    def sum(self, left, right):
        assert 0 <= left <= right <= self.n
        return self.sum_left(right) - self.sum_left(left)

    def lower_bound(self, x):
        """
        It returns max(i for i in range(n) if sum(0,i) < x).
        You can use it when all elements of the array is non-negative.
        """
        s = 0
        p = 0
        for i in reversed(range(self.n.bit_length())):
            if p | 1<<i <= self.n:
                d = self.data[p | 1<<i]
                if s + d < x:
                    s += d
                    p |= 1 << i
        return p
