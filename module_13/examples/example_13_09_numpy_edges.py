import numpy as np


def count_edges_between_paths(maze):
    """Count vertical and horizontal passage pairs using aligned slices."""
    path_mask = maze == 1
    vertical_pairs = path_mask[:-1, :] & path_mask[1:, :]
    horizontal_pairs = path_mask[:, :-1] & path_mask[:, 1:]

    vertical_edges = np.sum(vertical_pairs)
    horizontal_edges = np.sum(horizontal_pairs)
    return int(vertical_edges + horizontal_edges)


maze = np.array(
    [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    dtype=np.uint8
)

path_mask = maze == 1
vertical_pairs = path_mask[:-1, :] & path_mask[1:, :]
horizontal_pairs = path_mask[:, :-1] & path_mask[:, 1:]

print(vertical_pairs.astype(np.uint8))
print(horizontal_pairs.astype(np.uint8))
print(np.sum(vertical_pairs))
print(np.sum(horizontal_pairs))
print(count_edges_between_paths(maze))
