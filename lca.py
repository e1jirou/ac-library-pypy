class LowestCommonAncestor:
    def __init__(self, edges, root = 0):
        self.n = len(edges)
        self.edges = edges
        self.dfs(root)
        self.doubling()
    
    def dfs(self, root):
        parents = [-1] * self.n
        depths = [-1] * self.n
        depths[root] = 0
        todo = [root]
        while todo:
            a = todo.pop()
            for b in self.edges[a]:
                if depths[b] + 1:
                    continue
                parents[b] = a
                depths[b] = depths[a] + 1
                todo.append(b)
        self.parents = parents
        self.depths = depths
    
    def doubling(self):
        dbl = [self.parents]
        for _ in range(max(self.depths).bit_length()-1):
            parents = dbl[-1]
            new_parents = [-1] * self.n
            for i in range(self.n):
                if parents[i] + 1:
                    new_parents[i] = parents[parents[i]]
            dbl.append(new_parents)
        self.dbl = dbl
    
    def lca(self, a, b):
        if self.depths[a] < self.depths[b]:
            a, b = b, a
        for i in range((self.depths[a]-self.depths[b]).bit_length()):
            if self.depths[a]-self.depths[b] >> i & 1:
                a = self.dbl[i][a]
        if a == b:
            return a
        for i in range(self.depths[a].bit_length())[::-1]:
            if self.dbl[i][a] == self.dbl[i][b]:
                continue
            a, b = self.dbl[i][a], self.dbl[i][b]
        return self.dbl[0][a]
