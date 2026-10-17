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


def frontier_cells(frontier):
    """Collect allowed cell coordinates in row-major order."""
    rows, cols = frontier.shape
    cells = []

    for row in range(rows):
        for col in range(cols):
            if frontier[row, col] == 1:
                cells.append((row, col))

    return cells


def choose_next_frontier_cell(frontier):
    """Return one random allowed cell, or None if no cells are allowed."""
    cells = frontier_cells(frontier)
    if len(cells) == 0:
        return None

    index = np.random.randint(len(cells))
    return cells[index]


def growth_step(maze, frontier):
    """Open one cell using a frontier computed from the current maze."""
    cell = choose_next_frontier_cell(frontier)
    if cell is None:
        return False

    row, col = cell
    maze[row, col] = 1
    return True


maze = np.zeros((3, 4), dtype=np.uint8)
maze[1, 1] = 1
frontier = build_frontier(maze)

print(frontier_cells(frontier))
print(maze.sum())
print(growth_step(maze, frontier))
print(maze.sum())

# Recompute allowed openings before another growth step.
frontier = build_frontier(maze)

empty_frontier = np.zeros((3, 4), dtype=np.uint8)
print(choose_next_frontier_cell(empty_frontier))
print(growth_step(maze, empty_frontier))
