import numpy as np

gray = np.arange(24).reshape(6, 4)
blocks = gray.reshape(3, 2, 2, 2)

averages = blocks.mean(axis=(1, 3))

print(averages)
print("Before:", blocks.shape)
print("After:", averages.shape)
