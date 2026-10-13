# Repeat spatial axes while preserving RGB triples.
import numpy as np

COLORS = np.array([
    [245, 245, 245], [0, 0, 0], [255, 255, 255],
    [255, 0, 0], [0, 255, 0], [0, 0, 255],
], dtype=np.uint8)
matrix = np.array([[0, 3, 0], [5, 0, 3]], dtype=np.uint8)
CELL_SIZE = 2
rgb_small = COLORS[matrix]
rgb_rows = np.repeat(rgb_small, CELL_SIZE, axis=0)
rgb_big = np.repeat(rgb_rows, CELL_SIZE, axis=1)
print(rgb_small.shape)
print(rgb_rows.shape)
print(rgb_big.shape)
