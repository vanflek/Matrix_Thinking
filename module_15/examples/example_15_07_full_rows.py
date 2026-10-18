import numpy as np


blocks = np.array([
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
], dtype=np.uint8)

full_rows = np.all(blocks == 1, axis=1)
print("Full rows:", full_rows)

print("Rows to keep:")
print(blocks[~full_rows])

removed = full_rows.sum()
empty_rows = np.zeros((removed, blocks.shape[1]), dtype=np.uint8)
result = np.vstack((empty_rows, blocks[~full_rows]))

print("After:")
print(result)
