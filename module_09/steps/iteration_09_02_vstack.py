# Join matrices by rows
import numpy as np

a = np.array([
    [1, 2],
    [3, 4],
])

b = np.array([
    [5, 6],
    [7, 8],
])

print("a:")
print(a)
print("b:")
print(b)

vertical = np.vstack((a, b))

print(vertical)
print("Shape:", vertical.shape)
