import numpy as np

# One point-row in homogeneous coordinates.
point = np.array([[2, 3, 1]], dtype=float)

# Double X and halve Y; preserve the additional coordinate.
scale_matrix = np.array([
    [2, 0, 0],
    [0, 0.5, 0],
    [0, 0, 1],
], dtype=float)

scaled_point = point @ scale_matrix.T
print(scaled_point)
