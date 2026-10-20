# Return coordinates or None
import numpy as np


def spawn_apple(matrix):
    free_cells = np.argwhere(matrix == 0)

    if len(free_cells) == 0:
        return None

    index = np.random.randint(len(free_cells))
    return free_cells[index]


matrix = np.array([
    [5, 5, 5, 5],
    [5, 5, 5, 0],
    [5, 5, 5, 5],
], dtype=np.uint8)

apple = spawn_apple(matrix)

if apple is None:
    print("You win!")
else:
    print("Apple:", apple)
