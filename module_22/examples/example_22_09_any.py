import numpy as np

# Rows are samples; columns are rays.
walls = np.array([
    [False, False, False, False],
    [False, True,  False, False],
    [True,  False, False, False],
    [False, True,  True,  False],
    [True,  False, False, False],
])

has_wall = walls.any(axis=0)

print(has_wall)
print(has_wall.shape)
print(walls.any(axis=1))
print(walls.any())
print(has_wall.sum())
