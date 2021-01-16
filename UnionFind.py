# 0-indexed
class UnionFind:
    # if x is root: self.parents[x] = -(the number of the group nodes)
    # else: self.parents[x] = the parent of x
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    # return the parent of x
    def find(self, x):
        path = []
        while self.parents[x] >= 0:
            path.append(x)
            x = self.parents[x]
        for node in path:
            self.parents[node] = x
        return x

    # merge the group of x and the group of y
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

    # return the size of the group of x
    def size(self, x):
        return -self.parents[self.find(x)]

    # return whether x and y in a same group
    def same(self, x, y):
        return self.find(x) == self.find(y)

    # return [all nodes which is in the group of x]
    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    # return [all roots]
    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    # return the number of groups
    def group_count(self):
        return len(self.roots())

    # return {root: members of the group}
    def all_group_members(self):
        dic = dict()
        for i in range(self.n):
            p = self.find(i)
            if p in dic:
                dic[p].append(i)
            else:
                dic[p] = [i]
        return dic

    # return [sizes of all groups]
    def all_sizes(self):
        return [-x for x in self.parents if x < 0]
