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

right = P @ C_right
down = C_down @ P

print("Right:")
print(right)

print("Down:")
print(down)

both = C_down @ right

print("Right, then down:")
print(both)

edge = np.zeros((3, 5), dtype=int)
edge[2, 4] = 1

print("Right across the edge:")
print(edge @ C_right)

print("Down across the edge:")
print(C_down @ edge)
