# Use paired coordinate indices
import numpy as np

snake = np.array([
    [5, 2],
    [5, 3],
    [4, 3],
    [3, 3],
    [3, 4],
], dtype=np.int16)

matrix = np.zeros((8, 8), dtype=np.uint8)

snake_rows = snake[:, 0]
snake_cols = snake[:, 1]

matrix[snake_rows, snake_cols] = 5

print("Rows:", snake_rows)
print("Columns:", snake_cols)
print(matrix)

free_cells = np.argwhere(matrix == 0)
print("Free cells:", len(free_cells))
