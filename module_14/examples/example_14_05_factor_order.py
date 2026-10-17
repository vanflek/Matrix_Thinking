import numpy as np

A = np.array([
    [1, 2],
    [3, 4]
])

B = np.array([
    [0, 1],
    [1, 0]
])

print("A @ B:")
print(A @ B)

print("B @ A:")
print(B @ A)
