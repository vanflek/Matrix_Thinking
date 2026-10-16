import numpy as np

gray = np.arange(24).reshape(6, 4)
blocks = gray.reshape(3, 2, 2, 2)

print(blocks[1, :, 0, :])
