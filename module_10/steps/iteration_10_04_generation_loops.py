import numpy as np

matrix = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

rows, cols = matrix.shape
new_matrix = np.zeros_like(matrix)

for y in range(1, rows - 1):
    for x in range(1, cols - 1):
        block = matrix[y - 1:y + 2, x - 1:x + 2]
        alive_neighbors = int(np.sum(block)) - int(matrix[y, x])

        new_value = 0

        if matrix[y, x] == 1:
            if alive_neighbors == 2 or alive_neighbors == 3:
                new_value = 1
        else:
            if alive_neighbors == 3:
                new_value = 1

        new_matrix[y, x] = new_value

print("Current generation:")
print(matrix)

print("Next generation:")
print(new_matrix)
