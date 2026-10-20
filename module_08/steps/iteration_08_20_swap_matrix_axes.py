# Swap the two axes of a two-dimensional matrix.
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])
transposed = np.swapaxes(matrix, 0, 1)
print(transposed)
print(transposed.shape)
