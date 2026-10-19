import numpy as np

movement = np.array([3.0, 4.0])
length = np.linalg.norm(movement)
direction = movement / length

print(length)
print(direction)
print(np.linalg.norm(direction))
