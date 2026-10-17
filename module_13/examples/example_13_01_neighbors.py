import numpy as np


def get_neighbors4(row, col, rows, cols):
    """Return valid neighbors in the order: up, down, left, right."""
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))

    return neighbors


def count_path_neighbors(maze, row, col):
    """Count passages among valid neighbors of the selected cell."""
    rows, cols = maze.shape
    count = 0

    for neighbor_row, neighbor_col in get_neighbors4(row, col, rows, cols):
        if maze[neighbor_row, neighbor_col] == 1:
            count += 1

    return count


print(get_neighbors4(1, 1, 3, 4))
print(get_neighbors4(0, 0, 3, 4))
print(get_neighbors4(0, 1, 3, 4))

maze = np.array(
    [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 0],
    ],
    dtype=np.uint8
)

print(count_path_neighbors(maze, 1, 1))
print(count_path_neighbors(maze, 0, 1))
