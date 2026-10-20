import numpy as np

C_right = np.array([
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0]
])

v = np.array([10, 20, 30, 40, 50])

shifted = v @ C_right

print("Original:", v)
print("Shifted:", shifted)

player = np.array([0, 0, 1, 0, 0])

moved = player @ C_right

print("Before:", player)
print("After:", moved)

player = np.array([0, 0, 0, 0, 1])

moved = player @ C_right

print(moved)

# Compose two right shifts.
values = np.array([10, 20, 30, 40, 50])
C = C_right

after_first = values @ C
after_second = after_first @ C

C_two = C @ C
by_composition = values @ C_two

print("Two steps:", after_second)
print("Composed operator:", by_composition)
print("Same result:", np.array_equal(after_second, by_composition))
