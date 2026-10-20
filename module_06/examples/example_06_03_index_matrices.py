import numpy as np

matrix = np.zeros((3, 4), dtype=np.uint8)
row_indices, col_indices = np.indices(matrix.shape)

top = row_indices == 0
print(top)
print(row_indices)
print(col_indices)
