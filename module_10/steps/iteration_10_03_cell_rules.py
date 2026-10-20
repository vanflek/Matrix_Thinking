import numpy as np

matrix = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

y = 2
x = 2

print(matrix[y, x])


block = matrix[y - 1:y + 2, x - 1:x + 2]

print(block)


print(np.sum(block))


alive_neighbors = int(np.sum(block)) - int(matrix[y, x])

print(alive_neighbors)


new_value = 0


new_value = 0

if matrix[y, x] == 1:
    if alive_neighbors == 2 or alive_neighbors == 3:
        new_value = 1
else:
    if alive_neighbors == 3:
        new_value = 1

print(new_value)


for current_value in range(2):
    print("Current state:", current_value)

    for alive_neighbors in range(9):
        new_value = 0

        if current_value == 1:
            if alive_neighbors == 2 or alive_neighbors == 3:
                new_value = 1
        else:
            if alive_neighbors == 3:
                new_value = 1

        print(alive_neighbors, "->", new_value)
