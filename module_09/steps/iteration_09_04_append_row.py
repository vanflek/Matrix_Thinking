# Append a coordinate vector as one row
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

new_row = np.array([9, 10])

result = np.vstack((a, new_row))

print(result)
print("Shape:", result.shape)
