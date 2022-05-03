from collections import deque
from sys import setrecursionlimit
setrecursionlimit(10**9)
#from pypyjit import set_param
#set_param('max_unroll_recursion=-1')

class MaxFlow:
    """
    Reference
    https://github.com/atcoder/ac-library/blob/master/atcoder/maxflow.hpp
    https://github.com/atcoder/ac-library/blob/master/document_en/maxflow.md
    https://github.com/atcoder/ac-library/blob/master/document_ja/maxflow.md
    """
    def __init__(self, n):
        self.n = n
        self.pos = []
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        assert 0 <= fr < self.n
        assert 0 <= to < self.n
        assert 0 <= cap
        m = len(self.pos)
        self.pos.append((fr, len(self.g[fr])))
        fr_id = len(self.g[fr])
        to_id = len(self.g[to])
        if fr == to:
            to_id += 1
        self.g[fr].append(self._edge(to, to_id, cap))
        self.g[to].append(self._edge(fr, fr_id, 0))
        return m

    class edge:
        def __init__(self, fr, to, cap, flow):
            self.fr = fr
            self.to = to
            self.cap = cap
            self.flow = flow

    def get_edge(self, i):
        m = len(self.pos)
        assert 0 <= i < m
        e = self.g[self.pos[i][0]][self.pos[i][1]]
        re = self.g[e.to][e.rev]
        return self.edge(self.pos[i][0], e.to, e.cap+re.cap, re.cap)

    def edges(self):
        return [self.get_edge(i) for i in range(len(self.pos))]

    def change_edge(self, i, new_cap, new_flow):
        m = len(self.pos)
        assert 0 <= i < m
        assert 0 <= new_flow <= new_cap
        e = self.g[self.pos[i][0]][self.pos[i][1]]
        re = self.g[e.to][e.rev]
        e.cap = new_cap - new_flow
        re.cap = new_flow

    def flow(self, s, t, flow_limit):
        assert 0 <= s < self.n
        assert 0 <= t < self.n
        assert s != t
        level = [-1] * self.n
        it = [0] * self.n
        que = deque()

        def bfs():
            level[s] = 0
            que.clear()
            que.append(s)
            while que:
                v = que.popleft()
                for e in self.g[v]:
                    if e.cap == 0 or level[e.to] >= 0:
                        continue
                    level[e.to] = level[v] + 1
                    if e.to == t:
                        return
                    que.append(e.to)

        def dfs(v, up):
            if v == s:
                return up
            res = 0
            level_v = level[v]
            while it[v] < len(self.g[v]):
                i = it[v]
                it[v] += 1
                e = self.g[v][i]
                if level_v <= level[e.to] or self.g[e.to][e.rev].cap == 0:
                    continue
                d = dfs(e.to, min(up-res, self.g[e.to][e.rev].cap))
                if d <= 0:
                    continue
                self.g[v][i].cap += d
                self.g[e.to][e.rev].cap -= d
                res += d
                if res == up:
                    return res
            level[v] = self.n
            return res

        flow = 0
        while flow < flow_limit:
            level = [-1] * self.n
            bfs()
            if level[t] == -1:
                break
            it = [0] * self.n
            f = dfs(t, flow_limit - flow)
            if not f:
                break
            flow += f
        return flow

    def min_cut(self, s):
        visited = [0] * self.n
        que = deque()
        que.append(s)
        while que:
            p = que.popleft()
            visited[p] = 1
            for e in self.g[p]:
                if e.cap and not visited[e.to]:
                    visited[e.to] = 1
                    que.append(e.to)
        return visited

    class _edge:
        def __init__(self, to, rev, cap):
            self.to = to
            self.rev = rev
            self.cap = cap
