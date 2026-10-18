import numpy as np


fixed = np.array([
    [7, 0, 0],
    [0, 0, 0],
], dtype=np.uint8)

active = np.array([
    [0, 3, 0],
    [3, 3, 3],
], dtype=np.uint8)

# Deliberately copy the entire rectangle to demonstrate data loss.
wrong = fixed.copy()
wrong[:] = active
print("Whole rectangle:")
print(wrong)

# Copy only occupied cells and preserve the original block.
mask = active != 0
fixed[mask] = active[mask]
print("Occupied cells only:")
print(fixed)
