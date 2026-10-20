import numpy as np

matrix = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

print(matrix)


print(matrix[1, 2])
print(matrix[1, 1])


ROWS = 32
COLS = 64

matrix = np.zeros((ROWS, COLS), dtype=np.uint8)

print(matrix.shape)
print(np.sum(matrix))


matrix[15:17, 31:33] = 1

print(matrix[14:18, 30:34])
print(np.sum(matrix))
