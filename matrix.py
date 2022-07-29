def dot(a, b, mod):
    assert len(a[0]) == len(b)
    res = [[0] * len(a) for _ in range(len(b[0]))]
    for i in range(len(a)):
        a_i = a[i]
        for j in range(len(b[i])):
            tmp = 0
            for k in range(len(b)):
                tmp += a_i[k] * b[k][j]
                tmp %= mod
            res[i][j] = tmp
    return res

def matrix_power(a, exp, mod):
    assert len(a) == len(a[0])
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    for i in reversed(range(exp.bit_length())):
        res = dot(res, res)
        if exp>>i & 1:
            res = dot(res, a)
    return res
