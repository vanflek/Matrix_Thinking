import numpy as np

group = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
], dtype=np.uint8)

rows, cols = group.shape
Cx_right = np.zeros((cols, cols), dtype=np.uint8)
j = np.arange(cols)
Cx_right[j, (j + 1) % cols] = 1

Cy_down = np.zeros((rows, rows), dtype=np.uint8)
i = np.arange(rows)
Cy_down[(i + 1) % rows, i] = 1

shifted = Cy_down @ group @ Cx_right @ Cx_right
restored = Cy_down.T @ shifted @ Cx_right.T @ Cx_right.T

assert shifted.sum() == group.sum()
assert np.array_equal(restored, group)

print("Original:")
print(group)
print("Shifted:")
print(shifted)
print("Checks passed")
