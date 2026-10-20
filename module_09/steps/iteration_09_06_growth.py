# Keep the tail when eating an apple
import numpy as np

snake = np.array([
    [5, 2],
    [5, 3],
    [4, 3],
    [3, 3],
    [3, 4],
], dtype=np.int16)

movement = np.array([0, 1], dtype=np.int16)
apple = np.array([3, 5], dtype=np.int16)

new_head = snake[-1] + movement
eating = np.array_equal(new_head, apple)

snake = np.vstack((snake, new_head))

if not eating:
    snake = snake[1:]

print("Eating:", eating)
print(snake)
print("Length:", len(snake))
