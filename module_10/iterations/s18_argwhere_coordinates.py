import numpy as np

matrix = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

alive_cells = np.argwhere(matrix == 1)

print(alive_cells)


upper_neighbors = alive_cells + (-1, 0)

print(upper_neighbors)


offsets = np.array([
    [-1, -1],
    [-1,  0],
    [-1,  1],
    [ 0, -1],
    [ 0,  1],
    [ 1, -1],
    [ 1,  0],
    [ 1,  1],
])


neighbor_parts = []
for offset in offsets:
    neighbor_parts.append(alive_cells + offset)
neighbor_cells = np.vstack(neighbor_parts)
print("Recipient coordinates:")
print(neighbor_cells)
print("Shape:", neighbor_cells.shape)
