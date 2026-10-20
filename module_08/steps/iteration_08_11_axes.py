# An axis selects the array dimension affected by an operation.
import numpy as np

matrix = np.array([[10, 20, 30], [40, 50, 60]])
print(matrix.shape)
print(matrix[:, 1])
print(np.delete(matrix, 0, axis=0))
print(np.delete(matrix, 0, axis=1))
print(np.repeat(matrix, 2, axis=0).shape)
print(np.repeat(matrix, 2, axis=1).shape)
