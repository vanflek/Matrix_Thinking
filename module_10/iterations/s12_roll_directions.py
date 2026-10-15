import numpy as np

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

shifted = np.roll(matrix, 1, axis=0)

print(shifted)


print(np.roll(matrix, 1, axis=1))


print(np.roll(matrix, -1, axis=0))
print()
print(np.roll(matrix, -1, axis=1))


shifted = np.roll(matrix, 1, axis=0)

print(matrix[0, 1])
print(shifted[1, 1])
