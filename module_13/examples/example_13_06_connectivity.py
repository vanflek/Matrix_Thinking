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


def get_path_cells(maze):
    """Collect all passage coordinates without changing the maze."""
    rows, cols = maze.shape
    cells = []

    for row in range(rows):
        for col in range(cols):
            if maze[row, col] == 1:
                cells.append((row, col))

    return cells


def is_connected_paths(maze):
    """Check whether all passages are reachable from one starting cell."""
    path_cells = get_path_cells(maze)
    if len(path_cells) == 0:
        return False

    rows, cols = maze.shape
    start = path_cells[0]
    stack = [start]
    visited = {start}

    while stack:
        row, col = stack.pop()
        for neighbor in get_neighbors4(row, col, rows, cols):
            neighbor_row, neighbor_col = neighbor
            if maze[neighbor_row, neighbor_col] == 1 and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return len(visited) == len(path_cells)


connected = np.array(
    [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    dtype=np.uint8
)

disconnected = np.array(
    [
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0],
    ],
    dtype=np.uint8
)

print(is_connected_paths(connected))
print(is_connected_paths(disconnected))
print(is_connected_paths(np.zeros((2, 3), dtype=np.uint8)))
print(is_connected_paths(np.ones((1, 1), dtype=np.uint8)))
print(is_connected_paths(np.ones((2, 2), dtype=np.uint8)))
