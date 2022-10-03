class SlidingWindowAggregation:
    def __init__(self, op, e):
        self.op = op
        self.e = e
        self.data = []
        self.front = [e]
        self.back = [e]
 
    def __len__(self):
        return len(self.front) + len(self.back) - 2
 
    def push(self, x):
        self.data.append(x)
        self.back.append(self.op(self.back[-1], x))
 
    def pop(self):
        if len(self.front) == 1:
            self.move()
        self.front.pop()
 
    def move(self):
        self.back = [self.e]
        for x in reversed(self.data):
            self.front.append(self.op(x, self.front[-1]))
        self.data.clear()
 
    def get(self):
        return self.op(self.front[-1], self.back[-1])
