class BipartiteMatching:
    """
    Reference
    https://snuke.hatenablog.com/entry/2019/05/07/013609
    """
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.edges = [[] for _ in range(m)]

    def add_edge(self, u, v):
        assert 0 <= u < self.m
        assert 0 <= v < self.n
        self.edges[u].append(v)

    def flow(self):
        updated = True
        p = [-1] * self.m
        q = [-1] * self.n
        parent = [-1] * self.m
        root = [-1] * self.m
        queue = [0] * (2*self.m)

        while updated:
            updated = False
            left = right = 0
            # BFS
            for u in range(self.m):
                if p[u] == -1:
                    root[u] = u
                    queue[right] = u
                    right += 1
            while left < right:
                u = queue[left]
                left += 1
                if p[root[u]] != -1:
                    continue
                for v in self.edges[u]:
                    if q[v] == -1:
                        # found a path
                        while v != -1:
                            q[v] = u
                            p[u], v = v, p[u]
                            u = parent[u]
                        updated = True
                        break
                    w = q[v]
                    if parent[w] == -1:
                        parent[w] = u
                        root[w] = root[u]
                        queue[right] = w
                        right += 1
            if updated:
                for u in range(self.m):
                    parent[u] = root[u] = -1

        matching = []
        for u in range(self.m):
            if p[u] != -1:
                matching.append((u, p[u]))
        return matching
