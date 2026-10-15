import numpy as np


def life_calculation_roll(matrix):
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

    alive = matrix == 1
    survive = alive & ((neighbors == 2) | (neighbors == 3))
    born = (~alive) & (neighbors == 3)

    new_matrix = np.zeros_like(matrix)
    new_matrix[survive | born] = 1

    # Keep the outer border empty.
    new_matrix[0, :] = 0
    new_matrix[-1, :] = 0
    new_matrix[:, 0] = 0
    new_matrix[:, -1] = 0

    return new_matrix


matrix = np.zeros((15, 21), dtype=np.uint8)

matrix[4:6, 6:8] = 1
print("Block:", np.array_equal(life_calculation_roll(matrix), matrix))

matrix.fill(0)
matrix[7, 9:12] = 1
first = life_calculation_roll(matrix)
second = life_calculation_roll(first)
print("Blinker:", np.array_equal(second, matrix))

matrix.fill(0)
matrix[4:7, 6:9] = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
])
before = np.argwhere(matrix == 1)

for step in range(4):
    matrix = life_calculation_roll(matrix)

after = np.argwhere(matrix == 1)
print("Before:")
print(before)
print("After:")
print(after)
print("Displacement:")
print(after - before)
