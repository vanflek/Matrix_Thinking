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


def count_edges_between_paths(maze):
    """Count each connection once by looking only down and right."""
    rows, cols = maze.shape
    edges = 0

    for row in range(rows):
        for col in range(cols):
            if maze[row, col] != 1:
                continue

            if row + 1 < rows and maze[row + 1, col] == 1:
                edges += 1
            if col + 1 < cols and maze[row, col + 1] == 1:
                edges += 1

    return edges


def is_perfect_maze(maze):
    """A nonempty connected passage graph is a tree when E = V - 1."""
    vertices = len(get_path_cells(maze))
    if vertices == 0:
        return False

    if not is_connected_paths(maze):
        return False

    edges = count_edges_between_paths(maze)
    return edges == vertices - 1


tree = np.array(
    [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    dtype=np.uint8
)

cycle = np.ones((2, 2), dtype=np.uint8)

disconnected_cycle = np.array(
    [
        [1, 1, 0, 1],
        [1, 1, 0, 0],
    ],
    dtype=np.uint8
)

# Columns: vertices, edges, connected, perfect.
for maze in (tree, cycle, disconnected_cycle):
    print(
        len(get_path_cells(maze)),
        count_edges_between_paths(maze),
        is_connected_paths(maze),
        is_perfect_maze(maze)
    )
