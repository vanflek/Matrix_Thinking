import numpy as np

# Rows: Ball, Book, Pencil.
# Columns: volume, ratio.
W = np.array([
    [3, -4],
    [2, -1],
    [-2, 3]
])

x = np.array([8, 1])

scores = W @ x

print(scores)
print("Input shape:", x.shape)
print("Output shape:", scores.shape)

x = np.array([8, 3])

scores = W @ x
print(scores)

x = np.array([1, 8])

scores = W @ x
print(scores)
