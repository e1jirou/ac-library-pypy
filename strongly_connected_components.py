def scc(edges):
    n = len(edges)
    ids = [len(edges[u]) for u in range(n)]
    visited = [0] * n
    ord = [0] * n
    label = n
    for u in range(n):
        if visited[u]:
            continue
        visited[u] = 1
        path = [u]
        while path:
            u = path[-1]
            if ids[u]:
                ids[u] -= 1
                v = edges[u][ids[u]]
                if not visited[v]:
                    visited[v] = 1
                    path.append(v)
            else:
                label -= 1
                ord[label] = u
                path.pop()
    r_edges = [[] for _ in range(n)]
    for u in range(n):
        for v in edges[u]:
            r_edges[v].append(u)
    groups = []
    visited = [0] * n
    for u in ord:
        if visited[u]:
            continue
        visited[u] = 1
        group = [u]
        idx = 0
        while idx < len(group):
            u = group[idx]
            idx += 1
            for v in r_edges[u]:
                if not visited[v]:
                    visited[v] = 1
                    group.append(v)
        groups.append(group)
    return groups
