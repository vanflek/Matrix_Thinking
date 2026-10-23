import time
import numpy as np

ROWS = 128
COLS = 128
REPEATS = 20
matrix = np.zeros((ROWS, COLS), dtype=np.uint8)

start = time.perf_counter()
for repeat in range(REPEATS):
    matrix[:, :] = 0
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                matrix[row, col] = 1
loop_time = (time.perf_counter() - start) / REPEATS

start = time.perf_counter()
for repeat in range(REPEATS):
    matrix[:, :] = 0
    matrix[::2, ::2] = 1
    matrix[1::2, 1::2] = 1
slice_time = (time.perf_counter() - start) / REPEATS

print("Loops: seconds per pattern", loop_time)
print("Slices: seconds per pattern", slice_time)
print("Time ratio", loop_time / slice_time)
