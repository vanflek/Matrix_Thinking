import numpy as np

matrix = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

y = 2
x = 2

print(matrix[y, x])


block = matrix[y - 1:y + 2, x - 1:x + 2]

print(block)


print(np.sum(block))


alive_neighbors = int(np.sum(block)) - int(matrix[y, x])

print(alive_neighbors)
