class PivotTree:
    """
    Reference
    https://qiita.com/Kiri8128/items/6256f8559f0026485d90
    """
    def __init__(self, n=60):
        self.n = n
        self.root = self.node(1<<n, 1<<n)

    def add(self, v): # vを追加する. vをすでに含む場合はエラー.
        v += 1
        nd = self.root

        while True:
            assert v != nd.value
            nd.size += 1            
            
            mi, ma = min(v,nd.value), max(v,nd.value)
            if mi < nd.pivot:
                nd.value = ma
                if nd.left:
                    nd = nd.left
                    v = mi
                else:
                    p = nd.pivot
                    nd.left = self.node(mi, p - (p&-p)//2)
                    break
            else:
                nd.value = mi
                if nd.right:
                    nd = nd.right
                    v = ma
                else:
                    p = nd.pivot
                    nd.right = self.node(ma, p + (p&-p)//2)
                    break
    
    def leftmost(self, nd):
        if nd.left:
            return self.leftmost(nd.left)
        return nd
    
    def rightmost(self, nd):
        if nd.right:
            return self.rightmost(nd.right)
        return nd
    
    def remove(self, v, nd=None, prev=None): # 値がvのノードを削除する. 値がvのノードがなければ-1を返す.
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
            self.remove(nd.value-1, nd.right, nd)
        else:
            nd.value = self.rightmost(nd.left).value
            self.remove(nd.value-1, nd.left, nd)
    
    def at(self, k): # 0-indexed で小さいほうからk番目の値を取得する.
        assert k < self.root.size - 1
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

    def size(self):
        return self.root.size - 1

    class node:
        def __init__(self, v, p):
            self.value = v
            self.pivot = p
            self.left = None
            self.right = None
            self.size = 1
