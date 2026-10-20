import numpy as np

gray = np.arange(24).reshape(6, 4)
blocks = gray.reshape(3, 2, 2, 2)

print(gray[3, 2])
print(blocks[1, 1, 1, 0])
print(blocks[1, :, 0, :])
