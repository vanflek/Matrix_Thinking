import numpy as np

ROWS = 2
COLS = 3

matrix = np.zeros((ROWS, COLS, 3), dtype=np.uint8)

print(matrix.shape)
print(matrix[0, 0])

BG_RGB = np.array([245, 245, 245], dtype=np.uint8)

matrix[:] = BG_RGB

print(matrix)
