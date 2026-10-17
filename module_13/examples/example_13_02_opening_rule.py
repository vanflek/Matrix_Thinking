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


def has_any_path_cells(maze):
    """Return True if the maze contains at least one passage."""
    return np.any(maze == 1)


def can_open_by_local_rule(maze, row, col):
    """Check a valid cell without changing the maze."""
    if maze[row, col] != 0:
        return False

    if not has_any_path_cells(maze):
        return True

    return count_path_neighbors(maze, row, col) == 1


maze = np.zeros((3, 3), dtype=np.uint8)
print(has_any_path_cells(maze))
print(can_open_by_local_rule(maze, 1, 1))

maze[1, 1] = 1
print(can_open_by_local_rule(maze, 1, 1))
print(can_open_by_local_rule(maze, 1, 2))
print(can_open_by_local_rule(maze, 0, 0))

# These passages create a bend connected to the center.
maze[0, 1] = 1
maze[0, 2] = 1
print(can_open_by_local_rule(maze, 1, 2))
