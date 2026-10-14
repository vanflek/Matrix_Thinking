# Compare coordinate representations
import numpy as np

matrix = np.array([
    [0, 0, 0, 0],
    [0, 5, 5, 0],
    [0, 0, 5, 0],
], dtype=np.uint8)

free_mask = matrix == 0

print(free_mask)

free_cells = np.argwhere(free_mask)

print(free_cells)
print("Count:", len(free_cells))

positions = np.where(free_mask)

print(positions[0])
print(positions[1])

apple = free_cells[5]
print("Apple:", apple)
