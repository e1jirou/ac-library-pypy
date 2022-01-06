# Strongly Connected Components
# 0-indexed

def scc(edges, reversed_edges):
    assert len(edges) == len(reversed_edges)
    n = len(edges)
    # correct orientations
    edge_indexes = [len(edges[node]) for node in range(n)]
    order = [0] * n
    order_idx = 0
    parents = [-1] * n
    for node in range(n):
        if not parents[node]+1:
            parents[node] = n
            while n - node:
                if edge_indexes[node]:
                    edge_indexes[node] -= 1
                    new_node = edges[node][edge_indexes[node]]
                    if not parents[new_node]+1:
                        parents[new_node] = node
                        node = new_node
                else:
                    order[order_idx] = node
                    order_idx += 1
                    node = parents[node]
    # reversed orientations
    groups = []
    seen = [1] * n
    for start in order[::-1]:
        if seen[start]:
            seen[start] = 0
            todo = [start]
            group = [start]
            while todo:
                node = todo.pop()
                for new_node in reversed_edges[node]:
                    if seen[new_node]:
                        seen[new_node] = 0
                        todo.append(new_node)
                        group.append(new_node)
            groups.append(group[::-1])
    return groups
