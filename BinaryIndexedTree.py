# Fenwick Tree
# 0-indexed
class BinaryIndexedTree:
    def __init__(self, n):
        #self.array = [0] * n
        self.size = n
        self.data = [0] * (n+1)

    def add(self, i, x):
        #assert 0 <= i < self.size
        #self.array[i] += x
        i += 1
        while i <= self.size:
            self.data[i] += x
            i += i & -i

    # return sum(self.array[0:i])
    def sum_left(self, i):
        #assert 0 <= i <= self.size
        res = 0
        while i > 0:
            res += self.data[i]
            i -= i & -i
        return res

    # return sum(array[left:right])
    def sum_range(self, left, right):
        #assert 0 <= left <= right <= self.size
        return self.sum_left(right) - self.sum_left(left)
