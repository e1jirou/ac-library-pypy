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
