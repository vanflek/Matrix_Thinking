import numpy as np


first = np.array([0, 1, 0, 1])
second = np.array([1, 0, 0, 1])

# Compare corresponding elements, then find one maximum value.
print("Elementwise maximum:", np.maximum(first, second))
print("Maximum of first:", np.max(first))
print("Sum:", first + second)
