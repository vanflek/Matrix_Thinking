import numpy as np

CELL_SIZE = 30
rows, columns = 5, 7

ray_y = np.array([
    [45.0, 45.0, 75.0],
    [45.0, -0.2, 150.0],
])
ray_x = np.array([
    [45.0, 75.0, 75.0],
    [210.0, 45.0, 75.0],
])

cell_y = (ray_y // CELL_SIZE).astype(int)
cell_x = (ray_x // CELL_SIZE).astype(int)
inside = (
    (cell_y >= 0) & (cell_y < rows) &
    (cell_x >= 0) & (cell_x < columns)
)

print(cell_y)
print(cell_x)
print(inside)
print(inside.sum(), inside.size)
