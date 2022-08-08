class PivotTree:
    """
    You can store multiple equal integers.

    Reference
    https://qiita.com/Kiri8128/items/6256f8559f0026485d90
    """
    def __init__(self, n=(1<<60)-2):
        assert 0 <= n
        self.n = n + 1
        self.log = self.n.bit_length()
        self.root = self.node(1<<self.log, 1<<self.log, None, 0)

    def __len__(self):
        return self.root.size

    def __contains__(self, v):
        assert 0 <= v < self.n
        v += 1
        return self.find(v - 1).value == v

    def __iter__(self):
        nd = self.begin()
        while nd is not self.root:
            yield nd
            nd = nd.next()

    def __getitem__(self, v):
        return self.find_by_order(v).get()

    def insert(self, v, c=1):
        """
        It adds an element v.
        It returns None.
        """
        assert 0 <= v < self.n
        assert 0 < c
        v += 1
        nd = self.root
        while True:
            if v == nd.value:
                # The tree already contains v.
                nd.count += c
                break
            if nd.value < v <= nd.pivot or nd.pivot <= v < nd.value:
                v, nd.value = nd.value, v
                c, nd.count = nd.count, c
            if v < nd.pivot:
                if nd.left:
                    nd = nd.left
                else:
                    p = nd.pivot
                    nd.left = self.node(v, p - (p&-p)//2, nd, c)
                    break
            else:
                if nd.right:
                    nd = nd.right
                else:
                    p = nd.pivot
                    nd.right = self.node(v, p + (p&-p)//2, nd, c)
                    break
        nd.update()

    def lt_max(self, v):
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

    def leq_max(self, v):
        """
        It returns the node with the highest value among nodes whose value is less than or equal to v.
        When there is no such node, it returns None.
        """
        return self.lt_max(v + 1)

    def gt_min(self, v):
        """
        It returns the node with the lowest value among nodes whose value is greater than v.
        When there is no such node, it returns the root.
        """
        assert v < self.n
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

    def geq_min(self, v):
        """
        It returns the node with the lowest value among nodes whose value is greater than or equal to v.
        When there is no such node, it returns the root.
        """
        return self.gt_min(v - 1)

    def max_element(self):
        """
        It returns the node with the highest value.
        When the container is empty, it returns the root.
        """
        if self.root.left:
            return self.root.left.rightmost()
        else:
            return self.root

    def min_element(self):
        """
        It returns the node with the lowest value.
        When the container is empty, it returns the root.
        """
        return self.root.leftmost()

    def max(self):
        """
        It returns the maximum value.
        When the container is empty, it returns -1.
        """
        if self.root.size == 0:
            return -1
        else:
            return self.max_element().get()

    def min(self):
        """
        It returns the maximum value.
        When the container is empty, it returns ((1<<self.n) - 1).
        """
        return self.min_element().get()

    def erase(self, v, c=float("inf"), nd=None):
        """
        It removes an element v.
        It returns the number of removed elements.
        """
        assert 0 <= v < self.n
        v += 1
        if not nd:
            nd = self.root
        while v != nd.value:
            if v < nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    # The container does not contain v.
                    return 0
            else:
                if nd.right:
                    nd = nd.right
                else:
                    # The container does not contain v.
                    return 0
        if c < nd.count:
            nd.count -= c
            nd.update()
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
            nd.parent.update()
        elif nd.right:
            move_nd = nd.right.leftmost()
            nd.value = move_nd.value
            nd.count = move_nd.count
            self.erase(nd.value - 1, float("inf"), nd.right)
        else:
            move_nd = nd.left.rightmost()
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
        return self.root.size == 0

    def find_by_order(self, k):
        """
        It returns the node which has the k-th smallest element.
        When k is greater than or equal to the container, it returns the root.
        """
        if k < 0:
            k = self.root.size + k
        if not 0 <= k < self.root.size:
            return self.root
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
        self.root = self.node(1<<self.log, 1<<self.log, None, 0)

    def find(self, v):
        """
        It returns the node with a value of v.
        When the container does not contain v, it returns the root.
        """
        assert 0 <= v < self.n
        v += 1
        nd = self.gt_min(v - 2)
        if nd.value == v:
            return nd
        else:
            return self.root

    def count(self, v):
        """
        It returns the number of v.
        """
        assert 0 <= v < self.n
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
        return self.min_element()

    def end(self):
        """
        It returns the last node.
        """
        return self.root

    def is_end(self, nd):
        """
        It returns True if nd is the last node, False otherwise.
        """
        return nd is self.root

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
            """
            It returns the real value.
            """
            return self.value - 1

        def update(self):
            """
            It updates the size of all ancestors.
            """
            nd = self
            while nd:
                nd.size = nd.count
                if nd.left:
                    nd.size += nd.left.size
                if nd.right:
                    nd.size += nd.right.size
                nd = nd.parent

        def leftmost(self):
            """
            It returns the descendant with the smallest value.
            """
            nd = self
            while nd.left:
                nd = nd.left
            return nd

        def rightmost(self):
            """
            It returns the descendant with the highest value.
            """
            nd = self
            while nd.right:
                nd = nd.right
            return nd

        def next(self):
            """
            It returns the next node.
            """
            nd = self
            if nd.right:
                return nd.right.leftmost()
            while nd.parent:
                if nd.value < nd.parent.value:
                    return nd.parent
                nd = nd.parent
            # nd is end()
            return nd

        def prev(self):
            """
            It returns the previous node.
            """
            nd = self
            if nd.left:
                return nd.left.rightmost()
            while nd.parent:
                if nd.parent.value < nd.value:
                    return nd.parent
                nd = nd.parent
            # nd is begin() - 1
            return nd

        def add(self, c):
            """
            It changes the count.
            """
            assert 0 < self.count + c
            self.count += c
            self.update()
