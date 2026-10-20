# Build occupancy before choosing an apple
import numpy as np


def fill_field(matrix, snake):
    matrix[:] = 0
    matrix[snake[:, 0], snake[:, 1]] = 5


def spawn_apple(matrix):
    free_cells = np.argwhere(matrix == 0)

    if len(free_cells) == 0:
        return None

    index = np.random.randint(len(free_cells))
    return free_cells[index]


matrix = np.zeros((3, 4), dtype=np.uint8)

snake = np.array([
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
    [1, 3],
    [1, 2],
    [1, 1],
    [1, 0],
    [2, 0],
    [2, 1],
    [2, 2],
], dtype=np.int16)

fill_field(matrix, snake)
apple = spawn_apple(matrix)

if apple is None:
    print("You win!")
else:
    row, col = apple
    matrix[row, col] = 3
    print("Apple:", apple)

print(matrix)
