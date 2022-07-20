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
