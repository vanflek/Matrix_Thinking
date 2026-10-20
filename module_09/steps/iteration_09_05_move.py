# Add a head and remove the old tail
import numpy as np

snake = np.array([
    [5, 2],
    [5, 3],
    [4, 3],
    [3, 3],
    [3, 4],
], dtype=np.int16)

movement = np.array([0, 1], dtype=np.int16)

print("Before:")
print(snake)

new_head = snake[-1] + movement
print("New head:", new_head)

snake = np.vstack((snake, new_head))
print("Head added:")
print(snake)

snake = snake[1:]
print("Tail removed:")
print(snake)

print("Shape:", snake.shape)
