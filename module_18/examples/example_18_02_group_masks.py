import numpy as np


enemies = np.zeros((3, 5, 7), dtype=bool)
enemies[0, 1, 1] = True
enemies[1, 2, 3] = True
enemies[2, 3, 5] = True
trail = np.zeros((5, 7), dtype=bool)
trail[2, 3] = True

overlaps = enemies & trail
print("Overlap shape:", overlaps.shape)
print("Any collision:", overlaps.any())
print("By enemy:", overlaps.any(axis=(1, 2)))
occupied = enemies.any(axis=0)
print("Occupied shape:", occupied.shape)
print("Occupied cells:", occupied.sum())
