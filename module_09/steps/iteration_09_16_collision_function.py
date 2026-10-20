# Check free cells, body and departing tail
import numpy as np


def hits_body(new_head, snake, eating):
    if eating:
        body = snake
    else:
        body = snake[1:]

    matches = body == new_head
    same_cell = matches.all(axis=1)

    return same_cell.any()


snake = np.array([
    [2, 1],
    [2, 2],
    [2, 3],
    [3, 3],
    [3, 2],
    [3, 1],
], dtype=np.int16)

print("Free cell:",
      hits_body(np.array([3, 0]), snake, False))

print("Body:",
      hits_body(np.array([3, 2]), snake, False))

print("Departing tail:",
      hits_body(np.array([2, 1]), snake, False))
