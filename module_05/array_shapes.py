import numpy as np

# The values are the same, but the arrays have different numbers of axes.
vector = np.array([1, 0, 1], dtype=np.uint8)
matrix = np.array([[1, 0, 1]], dtype=np.uint8)
print(vector)
print(vector.shape)
print(matrix)
print(matrix.shape)

# One index selects a vector component; two select a matrix element.
print(vector[1])
print(matrix[0, 1])
