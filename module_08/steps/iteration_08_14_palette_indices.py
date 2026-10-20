# Repeated integer indices select repeated RGB vectors.
import numpy as np

COLORS = np.array([
    [245, 245, 245], [0, 0, 0], [255, 255, 255],
    [255, 0, 0], [0, 255, 0], [0, 0, 255],
], dtype=np.uint8)

indices = np.array([3, 0, 3, 5, 0])
print(COLORS[indices])
