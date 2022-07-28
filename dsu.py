class DisjointSetUnion:
    """
    Reference
    https://github.com/atcoder/ac-library/blob/master/atcoder/dsu.hpp
    https://github.com/atcoder/ac-library/blob/master/document_en/dsu.md
    https://github.com/atcoder/ac-library/blob/master/document_ja/dsu.md
    """
    def __init__(self, n):
        self.n = n
        self.parent_or_size = [-1] * n

    def leader(self, a):
        # This is not a recursive function.
        assert 0 <= a < self.n
        path = []
        while 0 <= self.parent_or_size[a]:
            path.append(a)
            a = self.parent_or_size[a]
        for b in path:
            self.parent_or_size[b] = a
        return a

    def merge(self, a, b):
        assert 0 <= a < self.n
        assert 0 <= b < self.n
        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return x
        if -self.parent_or_size[x] < -self.parent_or_size[y]:
            x, y = y, x
        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        return x

    def same(self, a, b):
        assert 0 <= a < self.n
        assert 0 <= b < self.n
        return self.leader(a) == self.leader(b)

    def size(self, a):
        assert 0 <= a < self.n
        return -self.parent_or_size[self.leader(a)]

    def groups(self):
        leader_buf = [0] * self.n
        group_size = [0] * self.n
        for i in range(self.n):
            leader_buf[i] = self.leader(i)
            group_size[leader_buf[i]] += 1
        result = [[0] * group_size[i] for i in range(self.n)]
        for i in reversed(range(self.n)):
            group_size[leader_buf[i]] -= 1
            result[leader_buf[i]][group_size[leader_buf[i]]] = i
        return [v for v in result if v]
