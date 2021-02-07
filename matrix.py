mod = 10**9 + 7


def mat_transpose(A):
    B = [[0] * len(A) for _ in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            B[j][i] = A[i][j]
    return B


def mat_flatten(A):
    B = [0] * (len(A) * len(A[0]))
    for i in range(len(A)):
        for j in range(len(A[0])):
            B[len(A[0])*i + j] = A[i][j]
    return B


def vec_mul_vec(x, y):
    assert len(x) == len(y)
    z = [0] * len(x)
    for i in range(len(x)):
        z[i] = x[i] * y[i]
    return z


def mat_mul_vec(A, x):
    assert len(A[0]) == len(x)

    y = [0] * len(A)
    for i in range(len(A)):
        tmp = 0
        for j in range(len(x)):
            tmp += A[i][j] * x[j]
        y[i] = tmp

    return y


def mat_mul_mat(A, B):
    assert len(A[0]) == len(B)

    C = [[0] * len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):
        A_i = A[i]
        for j in range(len(B[0])):
            tmp = 0
            for k in range(len(B)):
                tmp += A_i[k] * B[k][j]
                tmp %= mod###
            C[i][j] = tmp

    return C


from copy import deepcopy
def mat_add_mat(A, B):
    assert len(A) == len(B) and len(A[0]) == len(B[0])
    C = deepcopy(A)
    for i in range(len(A)):
        for j in range(len(A[0])):
            C[i][j] += B[i][j]
    return C


def mat_power(A, exp):
    assert len(A) == len(A[0])

    dbl = [A]
    for i in range(exp.bit_length()-1):
        dbl.append(mat_mul_mat(dbl[i],dbl[i]))

    B = [[0] * len(A) for _ in range(len(A))]
    for i in range(len(A)):
        B[i][i] = 1

    for i in range(exp.bit_length()):
        if exp>>i & 1:
            B = mat_mul_mat(B, dbl[i])

    return B


### test ###
import numpy as np

A = np.random.randint(1, 10, (3,4))
B = np.random.randint(1, 10, (4,2))
C = np.random.randint(1, 10, (3,3))
D = np.random.randint(1, 10, (3,4))
x = np.random.randint(1, 10, 4)
y = np.random.randint(1, 10, 4)

def ndarray_to_list(A):
    if A.ndim == 1:
        return list(A)
    if A.ndim == 2:
        return [list(row) for row in A]

A_lis = ndarray_to_list(A)
B_lis = ndarray_to_list(B)
C_lis = ndarray_to_list(C)
D_lis = ndarray_to_list(D)
x_lis = ndarray_to_list(x)
y_lis = ndarray_to_list(y)

print(ndarray_to_list(A.T) == mat_transpose(A_lis))
print(ndarray_to_list(A.flatten()) == mat_flatten(A_lis))
print(ndarray_to_list(x * y) == vec_mul_vec(x_lis, y_lis))
print(ndarray_to_list(A @ x) == mat_mul_vec(A_lis, x_lis))
print(ndarray_to_list(A @ B) == mat_mul_mat(A_lis, B_lis))
print(ndarray_to_list(A + D) == mat_add_mat(A_lis, D_lis))
print(ndarray_to_list(np.linalg.matrix_power(C, 5)) == mat_power(C_lis, 5))

