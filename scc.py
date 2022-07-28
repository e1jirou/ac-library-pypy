from sys import setrecursionlimit
setrecursionlimit(1000000000)

class StronglyConnectedComponents:
    def __init__(self, n):
        self.n = n
        self.edges = []

    def add_edge(self, fr, to):
        self.edges.append((fr, to))

    def csr(self):
        # Compressed Sparse Row
        self.start = [0] * (self.n + 1)
        for u, _ in self.edges:
            self.start[u + 1] += 1
        for i in range(self.n):
            self.start[i+1] += self.start[i]
        counter = self.start.copy()
        self.elist = [0] * len(self.edges)
        for u, v in self.edges:
            self.elist[counter[u]] = v
            counter[u] += 1

    def dfs(self, v):
        self.low[v] = self.ord[v] = self.now_ord
        self.now_ord += 1
        self.visited[self.idx] = v
        self.idx += 1
        for i in range(self.start[v], self.start[v+1]):
            to = self.elist[i]
            if self.ord[to] == -1:
                self.dfs(to)
                self.low[v] = min(self.low[v], self.low[to])
            else:
                self.low[v] = min(self.low[v], self.ord[to])
        if self.low[v] == self.ord[v]:
            while True:
                self.idx -= 1
                u = self.visited[self.idx]
                self.ord[u] = self.n
                self.ids[u] = self.group_num
                if u == v:
                    break
            self.group_num += 1

    def scc_ids(self):
        self.csr()
        self.now_ord = self.group_num = 0
        self.visited = [0] * self.n
        self.idx = 0
        self.low = [0] * self.n
        self.ord = [-1] * self.n
        self.ids = [0] * self.n
        for i in range(self.n):
            if self.ord[i] == -1:
                self.dfs(i)
        for i in range(self.n):
            self.ids[i] = self.group_num - 1 - self.ids[i]

    def scc(self):
        self.scc_ids()
        counts = [0] * self.group_num
        for x in self.ids:
            counts[x] += 1
        groups = [[] for _ in range(self.group_num)]
        for i in range(self.group_num):
            groups[i] = [0] * counts[i]
        for i in reversed(range(self.n)):
            counts[self.ids[i]] -= 1
            groups[self.ids[i]][counts[self.ids[i]]] = i
        return groups
