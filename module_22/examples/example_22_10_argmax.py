import numpy as np

values = np.array([4, 9, 9, 2])
print(values.argmax())

walls = np.array([
    [False, False, False, False],
    [False, True,  False, False],
    [True,  False, False, False],
    [False, True,  True,  False],
    [True,  False, False, False],
])

has_wall = walls.any(axis=0)
first_hit = walls.argmax(axis=0)

print(has_wall)
print(first_hit)

starts_with_wall = np.array([True, False, True])
no_wall = np.array([False, False, False])

print(starts_with_wall.any(), starts_with_wall.argmax())
print(no_wall.any(), no_wall.argmax())
