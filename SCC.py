from copy import deepcopy

# Strongly Connected Components

def scc(edges, reversed_edges, store_edges=True):
    #assert len(edges) == len(reversed_edges)
    if store_edges:
        edges = deepcopy(edges)
    n = len(edges)
    
    # correct orientations
    order = [0] * n
    order_idx = 0
    parents = [-1] * n
    for node in range(n):
        if not parents[node]+1:
            parents[node] = n
            while n - node:
                if edges[node]:
                    new_node = edges[node].pop()
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