import numpy as np

def is_inside(position, shape):
    row, col = position
    rows, cols = shape
    return (
        row >= 0 and row < rows
        and col >= 0 and col < cols
    )

shape = (10, 18)
positions = np.array([
    [5, 9], [0, 0], [9, 17], [-1, 9],
    [10, 9], [5, -1], [5, 18],
])

for position in positions:
    print(position, is_inside(position, shape))
