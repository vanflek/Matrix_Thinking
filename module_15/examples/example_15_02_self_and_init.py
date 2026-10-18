import numpy as np


class Marker:
    def __init__(self, row, col):
        self.position = np.array([row, col])
        print("Initialized:", self.position)

    def move(self, drow, dcol):
        print("Move from:", self.position)
        self.position += np.array([drow, dcol])
        print("Move to:", self.position)


first = Marker(2, 3)
second = Marker(5, 1)

print("Through the instance:")
first.move(0, 1)

print("Through the class:")
Marker.move(first, 1, 0)

print("Final positions:")
print("first:", first.position)
print("second:", second.position)
