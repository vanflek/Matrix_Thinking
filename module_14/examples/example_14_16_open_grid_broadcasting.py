import numpy as np

ROWS = 3
COLS = 5

Y, X = np.ogrid[:ROWS, :COLS]

print("Y:")
print(Y)
print("Y shape:", Y.shape)

print("X:")
print(X)
print("X shape:", X.shape)

total = Y + X

print("Y + X:")
print(total)
print("Result shape:", total.shape)

numbers = np.array([10, 20, 30])
print(numbers + 5)
