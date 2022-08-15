class Rerooting:
    def __init__(self, n):
        self.n = n
        self.edges = [[] for _ in range(n)]

    def add_edge(self, u, v):
        self.edges[u].append(v)

    def dfs(self):
        parents = [-1] * self.n
        parents[self.root] = self.n
        children = [[] for _ in range(self.n)]
        todo = [self.root]
        order = []
        while todo:
            u = todo.pop()
            order.append(u)
            for v in self.edges[u]:
                if parents[v] == -1:
                    parents[v] = u
                    children[u].append(v)
                    todo.append(v)
        self.children = children
        self.order = order

    def bottom_up(self):
        dp = [None] * self.n
        lr = [[self.id] * (len(self.children[u])+1) for u in range(self.n)]
        rl = [[self.id] * (len(self.children[u])+1) for u in range(self.n)]
        for u in reversed(self.order):
            for i in range(len(self.children[u])):
                v = self.children[u][i]
                lr[u][i+1] = self.composition(lr[u][i], dp[v])
            for i in reversed(range(len(self.children[u]))):
                v = self.children[u][i]
                rl[u][i] = self.composition(rl[u][i+1], dp[v])
            assert lr[u][-1] == rl[u][0]
            dp[u] = self.rooting(lr[u][-1])
        self.dp = dp
        self.lr = lr
        self.rl = rl

    def top_down(self):
        parents = [self.id] * self.n
        for u in self.order:
            p = self.composition(self.lr[u][-1], parents[u])
            self.dp[u] = self.rooting(p)
            for i in range(len(self.children[u])):
                v = self.children[u][i]
                p = self.composition(self.lr[u][i], self.rl[u][i+1])
                p = self.composition(p, parents[u])
                parents[v] = self.rooting(p)

    def rerooting(self, rooting, composition, id, root=0):
        self.rooting = rooting
        self.composition = composition
        self.id = id
        self.root = root
        self.dfs()
        self.bottom_up()
        self.top_down()
        return self.dp
