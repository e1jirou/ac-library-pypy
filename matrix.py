mod = 10**9 + 7

def matrix_mult(A, B):
    assert len(A[0]) == len(B)

    C = [[0] * len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):
        A_i = A[i]
        for j in range(len(B[0])):
            tmp = 0
            for k in range(len(B)):
                tmp += A_i[k] * B[k][j]
                tmp %= mod
            C[i][j] = tmp

    return C

def matrix_power(A, exp):
    assert len(A) == len(A[0])

    dbl = [A]
    for i in range(exp.bit_length()-1):
        dbl.append(matrix_mult(dbl[i],dbl[i]))

    B = [[0] * len(A) for _ in range(len(A))]
    for i in range(len(A)):
        B[i][i] = 1

    for i in range(exp.bit_length()):
        if exp>>i & 1:
            B = matrix_mult(B,dbl[i])

    return B

