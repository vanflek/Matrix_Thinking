import numpy as np

A = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 1, 2, 3]
])

B = np.array([
    [2, 0, 1, 3],
    [1, 2, 0, 1],
    [0, 5, 2, 1]
])

C = A * B

print(C)

B[1, 2] = 3

C = A * B
print(C)
