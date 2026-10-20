# Choose a free cell after checking the result
import numpy as np

matrix = np.array([
    [0, 0, 0, 0],
    [0, 5, 5, 0],
    [0, 0, 5, 0],
], dtype=np.uint8)

free_mask = matrix == 0

print(free_mask)

free_cells = np.argwhere(free_mask)

print(free_cells)
print("Count:", len(free_cells))

if len(free_cells) > 0:
    index = np.random.randint(len(free_cells))
    apple = free_cells[index]

    print("Index:", index)
    print("Apple:", apple)
else:
    print("You win!")
