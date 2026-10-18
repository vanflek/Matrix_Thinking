import numpy as np


class Marker:
    def __init__(self, row, col):
        # Each instance gets its own position array.
        self.position = np.array([row, col])

    def move(self, drow, dcol):
        # Update the position of this particular instance.
        self.position += np.array([drow, dcol])


first = Marker(2, 3)
second = Marker(5, 1)

print("Before:")
print("first:", first.position)
print("second:", second.position)

first.move(0, 1)
first.move(1, 0)

print("After moving first:")
print("first:", first.position)
print("second:", second.position)
