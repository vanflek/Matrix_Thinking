import numpy as np


def life_calculation(matrix):
    rows, cols = matrix.shape
    new_matrix = np.zeros_like(matrix)

    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            block = matrix[y - 1:y + 2, x - 1:x + 2]
            alive_neighbors = int(np.sum(block)) - int(matrix[y, x])

            new_value = 0

            if matrix[y, x] == 1:
                if alive_neighbors == 2 or alive_neighbors == 3:
                    new_value = 1
            else:
                if alive_neighbors == 3:
                    new_value = 1

            new_matrix[y, x] = new_value

    return new_matrix


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


matrix = np.zeros((7, 7), dtype=np.uint8)

matrix[1:4, 1:4] = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
], dtype=np.uint8)

next_loops = life_calculation(matrix)
next_roll = life_calculation_roll(matrix)

print(np.array_equal(next_loops, next_roll))


world_loops = matrix.copy()
world_roll = matrix.copy()
all_equal = True

for generation in range(20):
    world_loops = life_calculation(world_loops)
    world_roll = life_calculation_roll(world_roll)

    all_equal = all_equal and np.array_equal(
        world_loops,
        world_roll,
    )

print(all_equal)
