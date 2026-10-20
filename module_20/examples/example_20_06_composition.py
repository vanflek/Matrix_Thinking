import numpy as np

point = np.array([[2, 1, 1]], dtype=float)
scale_matrix = np.array([[2, 0, 0], [0, 0.5, 0], [0, 0, 1]])
# A counterclockwise quarter-turn, written with exact coefficients.
rotation_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
translation_matrix = np.array([[1, 0, 5], [0, 1, -2], [0, 0, 1]])

scaled_point = point @ scale_matrix.T
rotated_point = scaled_point @ rotation_matrix.T
sequential_result = rotated_point @ translation_matrix.T
transform_matrix = translation_matrix @ rotation_matrix @ scale_matrix
combined_result = point @ transform_matrix.T

print(scaled_point)
print(rotated_point)
print(sequential_result)
print(combined_result)
