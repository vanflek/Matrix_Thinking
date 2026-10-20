import numpy as np

counts = np.zeros(5, dtype=int)


indices = np.array([2, 2, 2])

for index in indices:
    counts[index] += 1

print(counts)


counts = np.zeros(5, dtype=int)

counts[indices] += 1

print(counts)


counts = np.zeros(5, dtype=int)

np.add.at(counts, indices, 1)

print(counts)


counts = np.array([0, 0, 10, 0, 0])

np.add.at(counts, indices, 2)

print(counts)


counts = np.zeros((4, 5), dtype=int)

ys = np.array([1, 1, 1, 2])
xs = np.array([2, 2, 2, 3])

np.add.at(counts, (ys, xs), 1)

print(counts)
