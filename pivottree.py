class PivotTree:
    """
    Reference
    https://qiita.com/Kiri8128/items/6256f8559f0026485d90

    You can store multiple equal integers.
    """
    def __init__(self, max_value=1<<60):
        self.n = (max_value + 1).bit_length()
        self.root = self.node(1<<self.n, 1<<self.n, None, 0)

    class node:
        def __init__(self, v, p, parent, c):
            self.value = v
            self.pivot = p
            self.left = None
            self.right = None
            self.parent = parent
            self.size = c
            self.count = c

        def get(self):
            return self.value - 1

    def update(self, nd):
        while nd:
            nd.size = nd.count
            if nd.left:
                nd.size += nd.left.size
            if nd.right:
                nd.size += nd.right.size
            nd = nd.parent

    def insert(self, v, c=1):
        """
        It adds an element v.
        It returns None.
        """
        assert 0 <= v < 1<<self.n
        assert 0 < c
        v += 1
        nd = self.root
        while True:
            if v == nd.value:
                # The tree already contains v.
                nd.count += c
                break
            if v < nd.value:
                mi_v = v
                ma_v = nd.value
                mi_c = c
                ma_c = nd.count
            else:
                mi_v = nd.value
                ma_v = v
                mi_c = nd.count
                ma_c = c
            if mi_v < nd.pivot:
                nd.value = ma_v
                nd.count = ma_c
                if nd.left:
                    nd = nd.left
                    v = mi_v
                    c = mi_c
                else:
                    p = nd.pivot
                    nd.left = self.node(mi_v, p - (p&-p)//2, nd, mi_c)
                    break
            else:
                nd.value = mi_v
                nd.count = mi_c
                if nd.right:
                    nd = nd.right
                    v = ma_v
                    c = ma_c
                else:
                    p = nd.pivot
                    nd.right = self.node(ma_v, p + (p&-p)//2, nd, ma_c)
                    break
        self.update(nd)

    def find_l(self, v):
        """
        It returns the node with the highest value among nodes whose value is less than v.
        When there is no such node, it returns None.
        """
        v += 1
        nd = self.root
        prev = None
        while True:
            if v <= nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    return prev
            else:
                prev = nd
                if nd.right:
                    nd = nd.right
                else:
                    return prev

    def find_r(self, v):
        """
        It returns the node with the lowest value among nodes whose value is greater than v.
        When there is no such node, it returns the root.
        """
        assert v < 1<<self.n
        v += 1
        nd = self.root
        prev = None
        while True:
            if v < nd.value:
                prev = nd
                if nd.left:
                    nd = nd.left
                else:
                    return prev
            else:
                if nd.right:
                    nd = nd.right
                else:
                    return prev

    def leftmost(self, nd):
        while nd.left:
            nd = nd.left
        return nd

    def rightmost(self, nd):
        while nd.right:
            nd = nd.right
        return nd

    @property
    def max_element(self):
        """
        It returns the node with the highest value.
        When the container is empty, it returns the root.
        """
        if self.empty():
            return self.root
        else:
            return self.rightmost(self.root.left)

    @property
    def min_element(self):
        """
        It returns the node with the lowest value.
        When the container is empty, it returns the root.
        """
        return self.leftmost(self.root)

    @property
    def max(self):
        """
        It returns the maximum value.
        When the container is empty, it returns -1.
        """
        if self.empty():
            return -1
        else:
            return self.max_element.get()

    @property
    def min(self):
        """
        It returns the maximum value.
        When the container is empty, it returns ((1<<self.n) - 1).
        """
        return self.min_element.get()

    def erase(self, v, c=float("inf"), nd=None):
        """
        It removes an element v.
        It returns the number of removed elements.
        """
        assert 0 <= v < 1<<self.n
        v += 1
        if not nd:
            nd = self.root
        while v != nd.value:
            if v < nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    # The tree does not contain v.
                    return 0
            else:
                if nd.right:
                    nd = nd.right
                else:
                    # The tree does not contain v.
                    return 0
        if c < nd.count:
            nd.count -= c
            self.update(nd)
            return c
        res = nd.count
        if not nd.left and not nd.right:
            if not nd.parent.left:
                nd.parent.right = None
            elif not nd.parent.right:
                nd.parent.left = None
            elif nd.pivot == nd.parent.left.pivot:
                nd.parent.left = None
            else:
                nd.parent.right = None
            self.update(nd.parent)
        elif nd.right:
            move_nd = self.leftmost(nd.right)
            nd.value = move_nd.value
            nd.count = move_nd.count
            self.erase(nd.value - 1, float("inf"), nd.right)
        else:
            move_nd = self.rightmost(nd.left)
            nd.value = move_nd.value
            nd.count = move_nd.count
            self.erase(nd.value - 1, float("inf"), nd.left)
        return res

    def size(self):
        """
        It returns the number of elements.
        """
        return self.root.size

    def empty(self):
        """
        It returns True if the container is empty, False otherwise.
        """
        return self.size() == 0

    def find_by_order(self, k):
        """
        It returns the node which has the k-th smallest element.
        When the tree size is k or less, it returns -1.
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
            elif k < left_size + nd.count:
                return nd
            else:
                k -= left_size + nd.count
                nd = nd.right

    def clear(self):
        """
        It removes all elements.
        """
        self.root = self.node(1<<self.n, 1<<self.n, None, 0)

    def find(self, v):
        """
        It returns the node with a value of v.
        When the container does not contain v, it returns the root.
        """
        assert 0 <= v < 1<<self.n
        v += 1
        nd = self.find_r(v - 2)
        if nd.value == v:
            return nd
        else:
            return self.root

    def contains(self, v):
        """
        It returns True if the container contains v, False otherwise.
        """
        assert 0 <= v < 1<<self.n
        v += 1
        return self.find(v - 1).value == v

    def count(self, v):
        """
        It returns the number of v.
        """
        assert 0 <= v < 1<<self.n
        v += 1
        nd = self.find(v - 1)
        if nd.value == v:
            return nd.count
        else:
            return 0

    def begin(self):
        """
        It returns the first node.
        """
        return self.min_element

    def end(self):
        """
        It returns the last node.
        """
        return self.root

    def next(self, nd):
        """
        It returns the next node.
        """
        while nd is not self.root:
            if nd.right:
                return self.leftmost(nd.right)
            nd = nd.parent
        return nd

    def prev(self, nd):
        """
        It returns the previous node.
        """
        while nd is not self.root:
            if nd.left:
                return self.rightmost(nd.left)
            nd = nd.parent
        return nd

    def index(self, v):
        """
        It returns the number of nodes whose value is less than v.
        """
        v += 1
        nd = self.root
        cnt = 0
        while nd:
            if nd.value < v:
                if nd.left:
                    cnt += nd.left.size
                cnt += nd.count
                nd = nd.right
            else:
                nd = nd.left
        return cnt

    def is_end(self, nd):
        """
        It returns True if nd is the last node, False otherwise.
        """
        return nd is self.root
