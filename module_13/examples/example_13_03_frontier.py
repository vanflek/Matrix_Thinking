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


def build_frontier(maze):
    """Mark every cell that can be opened in the current maze."""
    rows, cols = maze.shape
    frontier = np.zeros_like(maze)

    for row in range(rows):
        for col in range(cols):
            if can_open_by_local_rule(maze, row, col):
                frontier[row, col] = 1

    return frontier


maze = np.array(
    [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
    dtype=np.uint8
)

frontier = build_frontier(maze)
print(maze)
print(frontier)
