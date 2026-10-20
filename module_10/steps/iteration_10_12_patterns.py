import numpy as np


def life_calculation(matrix):
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

    return new_matrix


matrix = np.zeros((15, 21), dtype=np.uint8)

matrix[4:6, 6:8] = 1
print("Block:", np.array_equal(life_calculation(matrix), matrix))

matrix.fill(0)
matrix[7, 9:12] = 1
first = life_calculation(matrix)
second = life_calculation(first)
print("Blinker:", np.array_equal(second, matrix))

matrix.fill(0)
matrix[4:7, 6:9] = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
])
before = np.argwhere(matrix == 1)

for step in range(4):
    matrix = life_calculation(matrix)

after = np.argwhere(matrix == 1)
print("Before:")
print(before)
print("After:")
print(after)
print("Displacement:")
print(after - before)
