import numpy as np

values = np.array([10, 20, 30, 40, 50])
size = len(values)

C = np.zeros((size, size), dtype=np.uint8)
j = np.arange(size)
C[j, (j + 1) % size] = 1

C_two = C @ C
by_steps = values @ C @ C
by_composition = values @ C_two
by_roll = np.roll(values, 2)

assert np.array_equal(by_steps, by_composition)
assert np.array_equal(by_composition, by_roll)
assert np.array_equal(C @ C.T, np.eye(size, dtype=np.uint8))

print("Two steps:", by_steps)
print("Composed operator:", by_composition)
print("np.roll:", by_roll)
print("Checks passed")
