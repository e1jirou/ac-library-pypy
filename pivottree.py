class PivotTree:
    """
    Reference
    https://qiita.com/Kiri8128/items/6256f8559f0026485d90
    """
    def __init__(self, n=60):
        self.n = n
        self.root = self.node(1<<n, 1<<n)

    class node:
        def __init__(self, v, p):
            self.value = v
            self.pivot = p
            self.left = None
            self.right = None
            self.size = 1

    def insert(self, v):
        """
        It adds an element v.
        It returns -1 if the tree already contains v, 0 otherwise.
        """
        assert 0 < v + 1 < self.root.value
        v += 1
        nd = self.root
        while True:
            if v == nd.value:
                return -1
            nd.size += 1
            mi = min(v, nd.value)
            ma = max(v, nd.value)
            if mi < nd.pivot:
                nd.value = ma
                if nd.left:
                    nd = nd.left
                    v = mi
                else:
                    p = nd.pivot
                    nd.left = self.node(mi, p - (p&-p)//2)
                    return 0
            else:
                nd.value = mi
                if nd.right:
                    nd = nd.right
                    v = ma
                else:
                    p = nd.pivot
                    nd.right = self.node(ma, p + (p&-p)//2)
                    return 0

    def leftmost(self, nd):
        if nd.left:
            return self.leftmost(nd.left)
        return nd

    def rightmost(self, nd):
        if nd.right:
            return self.rightmost(nd.right)
        return nd

    def erase(self, v, nd=None, prev=None):
        """
        It removes an element v.
        It returns 0 if the tree contains v, -1 otherwise.
        """
        v += 1
        if not nd:
            nd = self.root
        if not prev:
            prev = nd
        while v != nd.value:
            nd.size -= 1
            prev = nd
            if v < nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    return -1
            else:
                if nd.right:
                    nd = nd.right
                else:
                    return -1
        nd.size -= 1
        if not nd.left and not nd.right:
            if not prev.left:
                prev.right = None
            elif not prev.right:
                prev.left = None
            elif nd.pivot == prev.left.pivot:
                prev.left = None
            else:
                prev.right = None
        elif nd.right:
            nd.value = self.leftmost(nd.right).value
            self.erase(nd.value - 1, nd.right, nd)
        else:
            nd.value = self.rightmost(nd.left).value
            self.erase(nd.value - 1, nd.left, nd)

    def size(self):
        return self.root.size - 1

    def find_by_order(self, k):
        """
        It returns k-th value in ascending order with 0-indexed.
        It returns -1 if the size is smaller than k.
        """
        if self.size() <= k:
            return -1
        nd = self.root
        while True:
            if nd.left:
                left_size = nd.left.size
            else:
                left_size = 0
            if k < left_size:
                nd = nd.left
            elif k == left_size:
                break
            else:
                k -= left_size + 1
                nd = nd.right
        return nd.value - 1
