import numpy as np

morning = np.array([[1, 0, 2],
                    [0, 1, 1]])
evening = np.array([[0, 3, 1],
                    [2, 0, 1]])

total = morning + evening
print(total)


total_with_loops = np.zeros_like(morning)

for y in range(morning.shape[0]):
    for x in range(morning.shape[1]):
        total_with_loops[y, x] = morning[y, x] + evening[y, x]

print(total_with_loops)
print(np.array_equal(total, total_with_loops))


print(np.add(morning, evening))
print(np.sum(morning))


print(morning + 10)
print(morning)


import numpy as np

a = np.array([[250]], dtype=np.uint8)
b = np.array([[10]], dtype=np.uint8)

print(a + b)
print(a.astype(np.int16) + b.astype(np.int16))
