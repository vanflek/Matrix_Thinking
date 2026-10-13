# Repeat columns after repeating rows.
import numpy as np

matrix = np.array([[0, 3, 0], [5, 0, 3]], dtype=np.uint8)
repeated_rows = np.repeat(matrix, 2, axis=0)
repeated_cells = np.repeat(repeated_rows, 2, axis=1)
print(repeated_cells)
print(repeated_cells.shape)
