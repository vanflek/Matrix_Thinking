import numpy as np

# The local origin and the nose of the airplane.
points = np.array([[0, 0, 1], [105, 0, 1]], dtype=float)
rotation_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
translation_matrix = np.array([[1, 0, 100], [0, 1, 50], [0, 0, 1]])

rotate_then_translate = translation_matrix @ rotation_matrix
translate_then_rotate = rotation_matrix @ translation_matrix

print(points @ rotate_then_translate.T)
print(points @ translate_then_rotate.T)
