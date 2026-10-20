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


def life_calculation_argwhere(matrix):
    rows, cols = matrix.shape
    alive_cells = np.argwhere(matrix == 1)

    offsets = np.array([
        [-1, -1], [-1, 0], [-1, 1],
        [ 0, -1],          [ 0, 1],
        [ 1, -1], [ 1, 0], [ 1, 1],
    ])

    neighbor_parts = []

    for offset in offsets:
        shifted = alive_cells + offset
        neighbor_parts.append(shifted)

    neighbor_cells = np.vstack(neighbor_parts)

    inside = (
        (neighbor_cells[:, 0] >= 0)
        & (neighbor_cells[:, 0] < rows)
        & (neighbor_cells[:, 1] >= 0)
        & (neighbor_cells[:, 1] < cols)
    )
    neighbor_cells = neighbor_cells[inside]

    ys = neighbor_cells[:, 0]
    xs = neighbor_cells[:, 1]

    neighbors = np.zeros_like(matrix)
    np.add.at(neighbors, (ys, xs), 1)

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


cases = []

matrix = np.zeros((15, 21), dtype=np.uint8)
cases.append(("Empty", matrix.copy()))

matrix[7, 10] = 1
cases.append(("Single cell", matrix.copy()))

matrix.fill(0)
matrix[4:6, 6:8] = 1
cases.append(("Block", matrix.copy()))

matrix.fill(0)
matrix[7, 9:12] = 1
cases.append(("Blinker", matrix.copy()))

matrix.fill(0)
matrix[4:7, 6:9] = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
])
cases.append(("Glider", matrix.copy()))

matrix.fill(0)
matrix[1, 1:4] = 1
matrix[2, 1] = 1
cases.append(("Near border", matrix.copy()))

functions = [
    life_calculation,
    life_calculation_roll,
    life_calculation_argwhere,
]

all_ok = True

for name, initial in cases:
    current = initial.copy()

    for step in range(1, 11):
        results = []

        for function in functions:
            candidate_input = current.copy()
            result = function(candidate_input)

            if not np.array_equal(candidate_input, current):
                print(name, step, function.__name__, "changed its input")
                all_ok = False

            results.append(result)

        same = (
            np.array_equal(results[0], results[1])
            and np.array_equal(results[0], results[2])
        )

        if not same:
            print(name, step, "different results")
            all_ok = False

        current = results[0]

if all_ok:
    print("All checks passed.")
