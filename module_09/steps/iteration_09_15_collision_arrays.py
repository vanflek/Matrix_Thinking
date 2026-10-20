# Reduce component matches to a collision flag
import numpy as np

snake = np.array([
    [2, 1],
    [2, 2],
    [2, 3],
    [3, 3],
    [3, 2],
], dtype=np.int16)

movement = np.array([-1, 0], dtype=np.int16)
new_head = snake[-1] + movement

eating = False

if eating:
    body = snake
else:
    body = snake[1:]

matches = body == new_head
same_cell = matches.all(axis=1)
collision = same_cell.any()

print("Components:")
print(matches)
print("Same cell:", same_cell)
print("Collision:", collision)
