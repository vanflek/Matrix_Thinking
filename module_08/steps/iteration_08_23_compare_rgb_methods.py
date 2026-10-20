# A loop and integer indexing produce the same color data.
import numpy as np

COLORS = np.array([
    [245, 245, 245], [0, 0, 0], [255, 255, 255],
    [255, 0, 0], [0, 255, 0], [0, 0, 255],
], dtype=np.uint8)
matrix = np.array([[0, 3, 0], [5, 0, 3]], dtype=np.uint8)
rows, cols = matrix.shape
rgb_loop = np.zeros((rows, cols, 3), dtype=np.uint8)
for row in range(rows):
    for col in range(cols):
        rgb_loop[row, col] = COLORS[matrix[row, col]]
rgb_array = COLORS[matrix]
print(rgb_loop)
print(rgb_array)
