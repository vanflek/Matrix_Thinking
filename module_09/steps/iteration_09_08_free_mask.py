# Mark free cells with a Boolean mask
import numpy as np

matrix = np.array([
    [0, 0, 0, 0],
    [0, 5, 5, 0],
    [0, 0, 5, 0],
], dtype=np.uint8)

free_mask = matrix == 0

print(free_mask)
