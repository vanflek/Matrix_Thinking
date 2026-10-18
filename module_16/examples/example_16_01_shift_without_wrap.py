import numpy as np


matrix = np.array([
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

print("Original:")
print(matrix)

print("Cyclic shift right:")
print(np.roll(matrix, 1, axis=1))

right = np.zeros_like(matrix)
right[:, 1:] = matrix[:, :-1]
print("Shift right without wrapping:")
print(right)

left = np.zeros_like(matrix)
left[:, :-1] = matrix[:, 1:]
print("Shift left without wrapping:")
print(left)

down = np.zeros_like(matrix)
down[1:, :] = matrix[:-1, :]
print("Shift down without wrapping:")
print(down)
