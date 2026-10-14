# Coordinate matrix, tail and head
import numpy as np

snake = np.array([
    [5, 2],
    [5, 3],
    [4, 3],
    [3, 3],
    [3, 4],
], dtype=np.int16)

print(snake)
print("Shape:", snake.shape)

print("Tail:", snake[0])
print("Head:", snake[-1])
