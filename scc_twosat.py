class StronglyConnectedComponents:
    """
    Reference
    https://github.com/atcoder/ac-library/blob/master/atcoder/internal_csr.hpp
    https://github.com/atcoder/ac-library/blob/master/atcoder/internal_scc.hpp
    https://github.com/atcoder/ac-library/blob/master/atcoder/scc.hpp
    https://github.com/atcoder/ac-library/blob/master/document_en/scc.md
    https://github.com/atcoder/ac-library/blob/master/document_ja/scc.md
    """
    def __init__(self, n):
        self.n = n
        self.edges = []

    def add_edge(self, fr, to):
        self.edges.append((fr, to))

    def __csr(self):
        # Compressed Sparse Row
        start = [0] * (self.n + 1)
        for u, _ in self.edges:
            start[u + 1] += 1
        for i in range(self.n):
            start[i + 1] += start[i]
        counter = start.copy()
        elist = [0] * len(self.edges)
        for u, v in self.edges:
            elist[counter[u]] = v
            counter[u] += 1
        return start, elist

    def scc_ids(self):
        # scc_ids does not contain a recursive function.
        start, elist = self.__csr()
        now_ord = group_num = now_visited = now_stack = 0
        visited = [0] * self.n
        low = [0] * self.n
        ord = [-1] * self.n
        ids = [0] * self.n
        stack = [0] * self.n
        counter = start.copy()
        for i in range(self.n):
            if ord[i] != -1:
                continue
            # dfs
            low[i] = ord[i] = now_ord
            now_ord += 1
            visited[now_visited] = i
            now_visited += 1
            stack[now_stack] = i
            now_stack += 1
            while now_stack:
                v = stack[now_stack - 1]
                while counter[v] < start[v + 1]:
                    to = elist[counter[v]]
                    counter[v] += 1
                    if ord[to] == -1:
                        low[to] = ord[to] = now_ord
                        now_ord += 1
                        visited[now_visited] = to
                        now_visited += 1
                        stack[now_stack] = to
                        now_stack += 1
                        break
                    else:
                        low[v] = min(low[v], ord[to])
                if stack[now_stack - 1] != v:
                    continue
                if low[v] == ord[v]:
                    while True:
                        now_visited -= 1
                        u = visited[now_visited]
                        ord[u] = self.n
                        ids[u] = group_num
                        if u == v:
                            break
                    group_num += 1
                now_stack -= 1
                if now_stack:
                    low[stack[now_stack - 1]] = min(low[stack[now_stack - 1]], low[v])
        for i in range(self.n):
            ids[i] = group_num - 1 - ids[i]
        return group_num, ids

    def scc(self):
        group_num, ids = self.scc_ids()
        counts = [0] * group_num
        for x in ids:
            counts[x] += 1
        groups = [[] for _ in range(group_num)]
        for i in range(group_num):
            groups[i] = [0] * counts[i]
        for i in reversed(range(self.n)):
            counts[ids[i]] -= 1
            groups[ids[i]][counts[ids[i]]] = i
        return groups


class TwoSAT:
    """
    Reference
    https://github.com/atcoder/ac-library/blob/master/atcoder/twosat.hpp
    https://github.com/atcoder/ac-library/blob/master/document_en/twosat.md
    https://github.com/atcoder/ac-library/blob/master/document_ja/twosat.md
    """
    def __init__(self, n):
        self.n = n
        self._answer = [False] * n
        self.scc = StronglyConnectedComponents(2 * n)

    def add_clause(self, i, f, j, g):
        assert 0 <= i < self.n
        assert 0 <= j < self.n
        self.scc.add_edge(2 * i + 1 - f, 2 * j + g)
        self.scc.add_edge(2 * j + 1 - g, 2 * i + f)

    def satisfiable(self):
        id = self.scc.scc_ids()[1]
        for i in range(self.n):
            if id[2 * i] == id[2 * i + 1]:
                return False
            self._answer[i] = id[2 * i] < id[2 * i + 1]
        return True

    def answer(self):
        return self._answer
