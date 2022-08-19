class MaxQueue:
    def __init__(self, maxlen):
        self.maxlen = maxlen
        self.left_stack = [(0,0)] * maxlen
        self.right_stack = [(0,0)] * maxlen
        self.left = self.right = 0
 
    def __move(self):
        assert self.right == 0 and self.left
        self.left -= 1
        x = self.left_stack[self.left][0]
        self.right_stack[self.right] = (x, x)
        self.right += 1
        while self.left:
            self.left -= 1
            x = self.left_stack[self.left][0]
            self.right_stack[self.right] = (x, max(x, self.right_stack[self.right - 1][1]))
            self.right += 1
 
    def push(self, x):
        if self.left:
            self.left_stack[self.left] = (x, max(x, self.left_stack[self.left - 1][1]))
        else:
            self.left_stack[self.left] = (x, x)
        self.left += 1
 
    def pop(self):
        if self.right == 0:
            self.__move()
        self.right -= 1
        return self.right_stack[self.right][0]
 
    def max(self):
        if self.left and self.right:
            return max(self.left_stack[self.left - 1][1], self.right_stack[self.right - 1][1])
        elif self.left:
            return self.left_stack[self.left - 1][1]
        elif self.right:
            return self.right_stack[self.right - 1][1]


from heapq import heapify, heappush, heappop

class RemovableHeap:
    def __init__(self, data=None):
        if data:
            self.data = data
            heapify(self.data)
        else:
            self.data = []
        self.removed = []

    def __len__(self):
        return len(self.data) - len(self.removed)

    def min(self):
        while self.removed and self.data[0] == self.removed[0]:
            heappop(self.data)
            heappop(self.removed)
        assert not self.removed or self.data[0] < self.removed[0]
        return self.data[0]

    def push(self, x):
        heappush(self.data, x)

    def pop(self):
        self.min()
        return heappop(self.data)

    def remove(self, x):
        heappush(self.removed, x)
