import numpy as np

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

I3 = np.eye(3, dtype=int)
I2 = np.eye(2, dtype=int)

right_result = A @ I3
left_result = I2 @ A

print("Right multiplication:")
print(right_result)

print("Left multiplication:")
print(left_result)

print("Right unchanged:", np.array_equal(right_result, A))
print("Left unchanged:", np.array_equal(left_result, A))
