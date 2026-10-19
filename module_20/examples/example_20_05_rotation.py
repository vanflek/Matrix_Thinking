import numpy as np

point = np.array([[2, 1, 1]], dtype=float)
angle_degrees = 30.0
angle_radians = np.deg2rad(angle_degrees)
cos_angle = np.cos(angle_radians)
sin_angle = np.sin(angle_radians)

# This matrix is written for point-columns.
rotation_matrix = np.array([
    [cos_angle, -sin_angle, 0],
    [sin_angle, cos_angle, 0],
    [0, 0, 1],
], dtype=float)

# The point is stored as a row, so use the transposed matrix.
rotated_point = point @ rotation_matrix.T
print(rotated_point)
