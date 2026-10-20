import numpy as np

indices = np.array([0, 2, 4])
matrix = np.zeros((6, 6), dtype=np.uint8)

# Equal-length index arrays select corresponding pairs.
matrix[indices, indices] = 1
print("Three pairs:")
print(matrix)

# Clear the first result before comparing the second selection.
matrix.fill(0)
matrix[::2, ::2] = 1
print("Nine row-column intersections:")
print(matrix)
