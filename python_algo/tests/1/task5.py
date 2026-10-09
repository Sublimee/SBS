class Queue:
    def __init__(self):
        self.queue = []

    # O(1)
    def enqueue(self, item):
        self.queue.append(item)

    # O(1)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)