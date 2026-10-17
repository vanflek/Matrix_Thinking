import numpy as np

P = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
])

C_right = np.array([
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0]
])

C_down = np.array([
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0]
])

C_left = C_right.T
C_up = C_down.T

left = P @ C_left
up = C_up @ P

print("Left:")
print(left)

print("Up:")
print(up)

right = P @ C_right
restored_x = right @ C_left

down = C_down @ P
restored_y = C_up @ down

print("Restored X:", np.array_equal(restored_x, P))
print("Restored Y:", np.array_equal(restored_y, P))

print(np.array_equal(
    C_right @ C_left,
    np.eye(5, dtype=int)
))

print(np.array_equal(
    C_left @ C_right,
    np.eye(5, dtype=int)
))
