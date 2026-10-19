import numpy as np

maze = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
], dtype=np.uint8)

cell_y = np.array([
    [1, 1, 2],
    [1, -1, 5],
])
cell_x = np.array([
    [1, 2, 2],
    [7, 1, 2],
])

rows, columns = maze.shape
inside = (
    (cell_y >= 0) & (cell_y < rows) &
    (cell_x >= 0) & (cell_x < columns)
)

selected_y = cell_y[inside]
selected_x = cell_x[inside]
values = maze[selected_y, selected_x]
is_wall = values == 0

walls = np.zeros_like(inside)
walls[inside] = is_wall

print(selected_y)
print(selected_x)
print(values)
print(is_wall)
print(walls)
