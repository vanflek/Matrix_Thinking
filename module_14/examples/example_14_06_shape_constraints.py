import numpy as np

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

B = np.array([
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1]
])

C = A @ B

print(C)
print("Shape:", C.shape)

# Uncomment to observe the intentional shape error.
# print(B @ A)
