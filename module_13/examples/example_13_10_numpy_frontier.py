import numpy as np


def build_frontier(maze):
    """Build allowed openings from four bounded neighbor contributions."""
    path_mask = maze == 1
    wall_mask = maze == 0

    # The first passage may be opened in any wall cell.
    if not np.any(path_mask):
        return wall_mask.astype(np.uint8)

    neighbors = np.zeros_like(maze, dtype=np.uint8)
    neighbors[1:, :] += path_mask[:-1, :]
    neighbors[:-1, :] += path_mask[1:, :]
    neighbors[:, 1:] += path_mask[:, :-1]
    neighbors[:, :-1] += path_mask[:, 1:]

    frontier_mask = wall_mask & (neighbors == 1)
    return frontier_mask.astype(np.uint8)


maze = np.array(
    [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    dtype=np.uint8
)

path_mask = maze == 1
neighbors = np.zeros_like(maze, dtype=np.uint8)
neighbors[1:, :] += path_mask[:-1, :]
neighbors[:-1, :] += path_mask[1:, :]
neighbors[:, 1:] += path_mask[:, :-1]
neighbors[:, :-1] += path_mask[:, 1:]

print(neighbors)
print(build_frontier(maze))
print(build_frontier(np.zeros((2, 3), dtype=np.uint8)))
