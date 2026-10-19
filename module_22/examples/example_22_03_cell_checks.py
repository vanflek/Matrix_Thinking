import numpy as np

CELL_SIZE = 30

maze = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
], dtype=np.uint8)


def can_move(maze, position):
    rows, columns = maze.shape
    world_height = rows * CELL_SIZE
    world_width = columns * CELL_SIZE
    y, x = position

    if not (0 <= y < world_height
            and 0 <= x < world_width):
        return False

    row = int(y // CELL_SIZE)
    column = int(x // CELL_SIZE)
    return maze[row, column] == 1


positions = [
    [45.5, 75.2],    # A passage.
    [75.0, 75.0],    # A wall inside the map.
    [-0.2, 75.0],    # Above the map.
    [150.0, 75.0],   # At the excluded bottom boundary.
    [45.0, 210.0],   # At the excluded right boundary.
]

for position in positions:
    print(f"{position}: {can_move(maze, position)}")
