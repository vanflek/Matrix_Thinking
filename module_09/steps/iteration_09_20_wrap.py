# Check all four boundaries on a rectangular field
import numpy as np

matrix = np.zeros((4, 6), dtype=np.uint8)
field_size = np.array(matrix.shape)

head = np.array([2, 5], dtype=np.int16)
movement = np.array([0, 1], dtype=np.int16)
print("Right:", (head + movement) % field_size)

head = np.array([2, 0], dtype=np.int16)
movement = np.array([0, -1], dtype=np.int16)
print("Left:", (head + movement) % field_size)

head = np.array([3, 4], dtype=np.int16)
movement = np.array([1, 0], dtype=np.int16)
print("Down:", (head + movement) % field_size)

head = np.array([0, 4], dtype=np.int16)
movement = np.array([-1, 0], dtype=np.int16)
print("Up:", (head + movement) % field_size)
