import numpy as np

matrix = np.array([
    [[255,   0,   0], [0, 255,   0], [  0,   0, 255]],
    [[255, 255,   0], [0, 255, 255], [255,   0, 255]],
], dtype=np.uint8)

print(matrix.shape)

print(matrix[1, 2])

print(matrix[1, 2, 0])

print(matrix[:, :, 0])
