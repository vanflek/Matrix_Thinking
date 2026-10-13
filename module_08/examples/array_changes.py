import numpy as np


def clear_cell(field, row, col):
    field[row, col] = 0


matrix = np.array([[0, 3, 0], [5, 0, 3]])
print("Before:")
print(matrix)
result = clear_cell(matrix, 1, 2)
print("After:")
print(matrix)
print("Returned value:", result)

# Both names refer to the same array. Slice assignment changes its contents.
state = {"vel": np.array([0, 1], dtype=np.int16)}
movement = state["vel"]
movement[:] = (1, 0)
print("After slice assignment:", state["vel"])

# Rebinding the local name does not replace the array in the dictionary.
movement = np.array([0, -1], dtype=np.int16)
print("New movement array:", movement)
print("Direction still stored in state:", state["vel"])
