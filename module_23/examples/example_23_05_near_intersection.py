import numpy as np


near = 1.0
a = np.array([-2, 1, -1, 1], dtype=float)
b = np.array([4, 3, 5, 1], dtype=float)

t = (near - a[2]) / (b[2] - a[2])
intersection = a + t * (b - a)

print(f"t = {t:.3f}")
print(intersection)
