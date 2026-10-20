# Join matrices by columns
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

horizontal = np.hstack((a, b))

print(horizontal)
print("Shape:", horizontal.shape)
