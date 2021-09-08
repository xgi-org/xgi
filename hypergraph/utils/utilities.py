

class HypergraphCounter():
    def __init__(self):
        self._count = 0
    def __call__(self):
        temp = self._count
        self._count += 1
        return temp