import numpy as np

player = np.zeros((3, 5), dtype=np.uint8)
player[1, 2] = 1

cols = player.shape[1]

right = np.zeros((cols, cols), dtype=np.uint8)
j = np.arange(cols)
right[j, (j + 1) % cols] = 1

by_operator = player @ right
by_roll = np.roll(player, 1, axis=1)

print("Matrix operator:")
print(by_operator)

print("np.roll:")
print(by_roll)

print("Same result:", np.array_equal(by_operator, by_roll))
