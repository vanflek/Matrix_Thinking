import numpy as np

left = np.array([[0, 1], [2, 3]])
right = np.array([[1, 2], [3, 3]])

left_distance = np.array([
    [5.0, 35.0],
    [110.0, 0.0]
])
right_distance = np.array([
    [25.0, 5.0],
    [75.0, 0.0]
])

choose_left = left_distance <= right_distance
indices = np.where(choose_left, left, right)

print(choose_left)
print(indices)
