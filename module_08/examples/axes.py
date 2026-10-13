import numpy as np

sample = np.array([[10, 20, 30], [40, 50, 60]])
print("Original matrix:")
print(sample)
print("Shape:", sample.shape)
print("Along axis 0, column 1 fixed:", sample[:, 1])
print("Along axis 1, row 1 fixed:", sample[1, :])

# Each operation starts from the original sample.
print("Delete row 1:")
print(np.delete(sample, 1, axis=0))
print("Delete column 1:")
print(np.delete(sample, 1, axis=1))
print("Repeat rows:")
print(np.repeat(sample, 2, axis=0))
print("Repeat columns:")
print(np.repeat(sample, 2, axis=1))
print("Swap row and column axes:")
print(np.swapaxes(sample, 0, 1))
print("Original unchanged:")
print(sample)
