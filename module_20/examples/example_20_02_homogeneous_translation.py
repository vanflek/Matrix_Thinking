import numpy as np

# Store one 2D point as a column with an additional coordinate of 1.
point = np.array([
    [2],
    [3],
    [1],
], dtype=float)

# Move the point 5 units right and 2 units down.
translation_matrix = np.array([
    [1, 0, 5],
    [0, 1, -2],
    [0, 0, 1],
], dtype=float)

translated_point = translation_matrix @ point
print(translated_point)
