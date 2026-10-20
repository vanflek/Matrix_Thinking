value = 1
print(value == 1)

import numpy as np

matrix = np.array([
    [0, 1, 0, 1],
    [1, 0, 0, 1]
], dtype=np.uint8)

mask = matrix == 1
print(mask)

print(matrix[mask])

matrix[mask] = 7
print(matrix)

print(mask)
print(matrix == 1)

# Other comparisons also produce Boolean masks.
print(matrix > 0)
print(matrix <= 1)
