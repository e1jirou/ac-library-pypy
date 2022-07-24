mod = 998244353

# transpose([[1,2],[3,4]]) == [[1,3],[2,4]]
def transpose(a):
    res = [[0] * len(a) for _ in range(len(a[0]))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            res[j][i] = a[i][j]
    return res

# dot_t(a, b) == a @ b.T
def dot_t(a, b):
    assert len(a[0]) == len(b[0])
    res = [[0] * len(b) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b)):
            for k in range(len(a[0])):
                res[i][j] += a[i][k] * b[j][k] % mod
            res[i][j] %= mod
    return res

# dot(a, b) == a @ b
def dot(a, b):
    return dot_t(a, transpose(b))

def matrix_power(a, exp):
    n = len(a)
    a = transpose(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    for i in reversed(range(exp.bit_length())):
        res = dot(res, res)
        if exp>>i & 1:
            res = dot_t(res, a)
    return res
