# Repeat complete rows along axis zero.
import numpy as np

matrix = np.array([[0, 3, 0], [5, 0, 3]], dtype=np.uint8)
repeated_rows = np.repeat(matrix, 2, axis=0)
print(repeated_rows)
print(repeated_rows.shape)
