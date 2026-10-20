# The array changes even though the function returns None.
import numpy as np

def clear_cell(field, row, col):
    field[row, col] = 0


matrix = np.array([[0, 1, 0], [0, 0, 1]])
result = clear_cell(matrix, 0, 1)
print(matrix)
print(result)
