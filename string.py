"""
Reference
https://github.com/atcoder/ac-library/blob/master/atcoder/string.hpp
https://github.com/atcoder/ac-library/blob/master/document_en/string.md
https://github.com/atcoder/ac-library/blob/master/document_ja/string.md
"""


def merge_sort(data, lt=lambda x,y: x < y):
    # stable sort
    n = len(data)
    res = data.copy()
    width = 1
    while width < n:
        tmp = 0
        for i in range(0, n, 2*width):
            l = i
            r = mid = min(n, i + width)
            end = min(n, i + 2*width)
            while l < mid and r < end:
                if lt(data[r], data[l]):
                    res[tmp] = data[r]
                    r += 1
                else:
                    res[tmp] = data[l]
                    l += 1
                tmp += 1
            while l < mid:
                res[tmp] = data[l]
                l += 1
                tmp += 1
            while r < end:
                res[tmp] = data[r]
                r += 1
                tmp += 1
        data, res = res, data
        width *= 2
    return data


def sa_naive(s):
    n = len(s)

    def cmp(l, r):
        if l == r:
            return False
        while l < n and r < n:
            if s[l] != s[r]:
                return s[l] < s[r]
            l += 1
            r += 1
        return l == n

    return merge_sort(list(range(n)), cmp)


def sa_doubling(s):
    n = len(s)
    rnk = s.copy()
    tmp = [0] * n
    sa = list(range(n))
    k = 1
    while k < n:

        def cmp(x, y):
            if rnk[x] != rnk[y]:
                return rnk[x] < rnk[y]
            rx = rnk[x + k] if x + k < n else -1
            ry = rnk[y + k] if y + k < n else -1
            return rx < ry

        sa = merge_sort(sa, cmp)
        tmp[sa[0]] = 0
        for i in range(n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (1 if cmp(sa[i - 1], sa[i]) else 0)
        tmp, rnk = rnk, tmp
        k *= 2
    return sa


# SA-IS, linear-time suffix array construction
# Reference:
# G. Nong, S. Zhang, and W. H. Chan,
# Two Efficient Algorithms for Linear Time Suffix Array Construction
THRESHOLD_NAIVE = 10
THRESHOLD_DOUBLING = 40
def sa_is(s, upper):
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        if s[0] < s[1]:
            return [0, 1]
        else:
            return [1, 0]
    if n < THRESHOLD_NAIVE:
        return sa_naive(s)
    if n < THRESHOLD_DOUBLING:
        return sa_doubling(s)
    sa = [0] * n
    ls = [False] * n
    for i in range(n-2, -1, -1):
        ls[i] = ls[i + 1] if s[i] == s[i + 1] else s[i] < s[i + 1]
    sum_l = [0] * (upper + 1)
    sum_s = [0] * (upper + 1)
    for i in range(n):
        if not ls[i]:
            sum_s[s[i]] += 1
        else:
            sum_l[s[i] + 1] += 1
    for i in range(upper + 1):
        sum_s[i] += sum_l[i]
        if i < upper:
            sum_l[i + 1] += sum_s[i]
    
    def induce(lms):
        for i in range(len(sa)):
            sa[i] = -1
        buf = sum_s.copy()
        for d in lms:
            if d == n:
                continue
            sa[buf[s[d]]] = d
            buf[s[d]] += 1
        buf = sum_l.copy()
        sa[buf[s[n - 1]]] = n - 1
        buf[s[n - 1]] += 1
        for i in range(n):
            v = sa[i]
            if v >= 1 and not ls[v - 1]:
                sa[buf[s[v - 1]]] = v - 1
                buf[s[v - 1]] += 1
        buf = sum_l.copy()
        for i in range(n - 1, -1, -1):
            v = sa[i]
            if v >= 1 and ls[v - 1]:
                buf[s[v - 1] + 1] -= 1
                sa[buf[s[v - 1] + 1]] = v - 1

    lms_map = [-1] * (n + 1)
    m = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = m
            m += 1
    lms = [0] * m
    now_lms = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms[now_lms] = i
            now_lms += 1
    lms = lms[:now_lms]
    induce(lms)
    if m:
        sorted_lms = [0] * m
        now_sorted_lms = 0
        for v in sa:
            if lms_map[v] != -1:
                sorted_lms[now_sorted_lms] = v
                now_sorted_lms += 1
        rec_s = [0] * m
        rec_upper = 0
        for i in range(1, m):
            l = sorted_lms[i-1]
            r = sorted_lms[i]
            end_l = lms[lms_map[l] + 1] if lms_map[l] + 1 < m else n
            end_r = lms[lms_map[r] + 1] if lms_map[r] + 1 < m else n
            same = True
            if end_l - l != end_r - r:
                same = False
            else:
                while l < end_l:
                    if s[l] != s[r]:
                        break
                    l += 1
                    r += 1
                if l == n or s[l] != s[r]:
                    same = False
            if not same:
                rec_upper += 1
            rec_s[lms_map[sorted_lms[i]]] = rec_upper
        rec_sa = sa_is(rec_s, rec_upper)
        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]
        induce(sorted_lms)
    return sa


def suffix_array(s, upper=None):
    if upper is not None:
        assert type(s[0]) == int
        assert 0 <= upper
        for d in s:
            assert 0 <= d <= upper
        return sa_is(s, upper)
    elif type(s[0]) == str:
        n = len(s)
        s2 = [ord(char) for char in s]
        return sa_is(s2, 255)
    else:
        n = len(s)
        idx = list(sorted(range(n), key=lambda x: s[x]))
        s2 = [0] * n
        now = 0
        for i in range(n):
            if i and s[idx[i - 1]] != s[idx[i]]:
                now += 1
            s2[idx[i]] = now
        return sa_is(s2, now)


# Reference:
# T. Kasai, G. Lee, H. Arimura, S. Arikawa, and K. Park,
# Linear-Time Longest-Common-Prefix Computation in Suffix Arrays and Its
# Applications
def lcp_array(s, sa):
    n = len(s)
    assert n >= 1
    if type(s[0]) == str:
        s2 = [ord(char) for char in s]
        return lcp_array(s2, sa)
    rnk = [0] * n
    for i in range(n):
        rnk[sa[i]] = i
    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        if h > 0:
            h -= 1
        if rnk[i] == 0:
            continue
        j = sa[rnk[i] - 1]
        while j + h < n and i + h < n:
            if s[j + h] != s[i + h]:
                break
            h += 1
        lcp[rnk[i] - 1] = h
    return lcp


# Reference:
# D. Gusfield,
# Algorithms on Strings, Trees, and Sequences: Computer Science and
# Computational Biology
def z_algorithm(s):
    n = len(s)
    if n == 0:
        return []
    if type(s[0]) == str:
        s2 = [ord(char) for char in s]
        return z_algorithm(s2)
    z = [0] * n
    j = 0
    for i in range(1, n):
        z[i] = 0 if j + z[j] <= i else min(j + z[j] - i, z[i - j])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if j + z[j] < i + z[i]:
            j = i
    z[0] = n
    return z
