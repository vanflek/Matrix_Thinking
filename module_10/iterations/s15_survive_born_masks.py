import numpy as np

matrix = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

up = np.roll(matrix, 1, axis=0)
down = np.roll(matrix, -1, axis=0)
left = np.roll(matrix, 1, axis=1)
right = np.roll(matrix, -1, axis=1)

up_left = np.roll(up, 1, axis=1)
up_right = np.roll(up, -1, axis=1)
down_left = np.roll(down, 1, axis=1)
down_right = np.roll(down, -1, axis=1)

neighbors = (
    up + down + left + right
    + up_left + up_right + down_left + down_right
)

print(neighbors)


alive = matrix == 1

survive = alive & ((neighbors == 2) | (neighbors == 3))
born = (~alive) & (neighbors == 3)

print("Survive:")
print(survive.astype(np.uint8))

print("Born:")
print(born.astype(np.uint8))


new_matrix = np.zeros_like(matrix)
new_matrix[survive | born] = 1


new_matrix[0, :] = 0
new_matrix[-1, :] = 0
new_matrix[:, 0] = 0
new_matrix[:, -1] = 0

print(new_matrix)
