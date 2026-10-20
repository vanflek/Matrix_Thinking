import numpy as np


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


matrix = np.zeros((5, 5), dtype=np.uint8)
matrix[2, 1:4] = 1

next_matrix = life_calculation_argwhere(matrix)
print(next_matrix)

restored_matrix = life_calculation_argwhere(next_matrix)
print(np.array_equal(restored_matrix, matrix))
