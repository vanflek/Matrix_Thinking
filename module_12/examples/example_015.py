import numpy as np

channel = np.array([
    [0, 0],
    [255, 255]
], dtype=np.uint8)

print(channel.mean())
