import numpy as np

matrix = np.array([
    [10, 11, 12, 13, 14],
    [20, 21, 22, 23, 24],
    [30, 31, 32, 33, 34]
])

print(matrix[1, :])

print(matrix[:, 2])

print(matrix[:, :])

print(matrix[0:2, 1:4])

print(matrix[1:-1, 1:-1])

matrix[0:2, 1:4] = 0
print(matrix)

for row in range(0, 2):
    for col in range(1, 4):
        matrix[row, col] = 0

matrix[:, :] = 0
print(matrix)

matrix[1:, 1:4] = 1
print(matrix)
