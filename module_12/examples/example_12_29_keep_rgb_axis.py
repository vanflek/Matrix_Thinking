import numpy as np

pixels = np.array([
    [[0, 0, 0], [200, 0, 0]],
    [[0, 100, 0], [0, 0, 100]]
], dtype=np.uint8)

blocks = pixels.reshape(1, 2, 1, 2, 3)

correct = blocks.mean(axis=(1, 3))
incorrect = blocks.mean(axis=(1, 3, 4))

print(correct)
print(correct.shape)

print(incorrect)
print(incorrect.shape)
