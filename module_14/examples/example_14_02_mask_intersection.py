import numpy as np

mask_a = np.array([
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
], dtype=np.uint8)

mask_b = np.array([
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0]
], dtype=np.uint8)

overlap = mask_a * mask_b

print(overlap)

print("Any overlap:", overlap.any())
print("Overlap cells:", np.sum(overlap))

intersection = (mask_a == 1) & (mask_b == 1)

print(np.array_equal(
    overlap,
    intersection.astype(np.uint8)
))
