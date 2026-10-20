import numpy as np


fixed = np.array([
    [0, 7, 0],
    [0, 0, 0],
], dtype=np.uint8)

candidate = np.array([
    [0, 3, 0],
    [3, 3, 3],
], dtype=np.uint8)

overlap = fixed * candidate
print(overlap)
print("Free:", not np.any(overlap))

fixed[0, 1] = 0
fixed[0, 0] = 7

overlap = fixed * candidate
print(overlap)
print("Free:", not np.any(overlap))
