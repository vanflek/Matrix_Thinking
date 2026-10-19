import numpy as np


vertex = np.array([0, 0, 1, 1], dtype=float)
scaling = np.diag([2.0, 1.0, 3.0, 1.0])

# Local-to-world orientation for yaw = 90 degrees.
orientation = np.array([
    [0, 0, -1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1],
], dtype=float)

print(vertex @ scaling @ orientation)
print(vertex @ orientation @ scaling)
