"""Compare the two checkerboard-building snippets from Module 6.

Install NumPy in your project's interpreter, then run this file in PyCharm
or use: python examples/example_06_02_benchmark_checkerboard.py
No Pygame window is opened. Results appear in the console.

This is a ready-to-run measuring tool. The chapter explains the two snippets;
understanding the timer implementation is not required for the exercises.
"""

import platform
from statistics import median
from timeit import Timer

import numpy as np


# Only these statements are timed: clearing and filling an existing array.
# Allocation, correctness checks, printing, and display are outside the timer.
LOOP_CODE = """
matrix[:, :] = 0

for row in range(ROWS):
    for col in range(COLS):
        if (row + col) % 2 == 0:
            matrix[row, col] = 1
"""

SLICE_CODE = """
matrix[:, :] = 0
matrix[::2, ::2] = 1
matrix[1::2, 1::2] = 1
"""

SHAPES = ((16, 16), (1024, 1024))
SERIES = 5

print(f"Python {platform.python_version()} | NumPy {np.__version__}")
print("Array dtype: uint8. Times are milliseconds per pattern build.")
print("Each result is the median of five timed series.")
print("Only clearing and filling are timed; allocation and display are excluded.")
print("Your measurements may differ from the chapter's example.")
print()
print(f"{'Shape':>12} {'Loops (ms)':>14} {'Slices (ms)':>14} {'Ratio':>10}")

for shape in SHAPES:
    # Both implementations use the same preallocated matrix for this size.
    matrix = np.zeros(shape, dtype=np.uint8)
    ROWS, COLS = matrix.shape
    context = {"matrix": matrix, "ROWS": ROWS, "COLS": COLS}
    loop_timer = Timer(LOOP_CODE, globals=context)
    slice_timer = Timer(SLICE_CODE, globals=context)

    # Warm up both snippets and verify equality before measuring them.
    loop_timer.timeit(number=1)
    loop_result = matrix.copy()
    slice_timer.timeit(number=1)
    if not np.array_equal(loop_result, matrix):
        raise RuntimeError("The two implementations produced different patterns.")

    # Choose enough calls to time small operations reliably (at least 0.2 s).
    # Each implementation may need a different number of calls per series.
    loop_calls, _ = loop_timer.autorange()
    slice_calls, _ = slice_timer.autorange()
    loop_samples = loop_timer.repeat(repeat=SERIES, number=loop_calls)
    slice_samples = slice_timer.repeat(repeat=SERIES, number=slice_calls)

    # Normalize by the number of calls, then convert seconds to milliseconds.
    loop_ms = median(loop_samples) / loop_calls * 1000
    slice_ms = median(slice_samples) / slice_calls * 1000
    ratio = loop_ms / slice_ms
    size_label = f"{ROWS} x {COLS}"
    print(f"{size_label:>12} {loop_ms:14.6f} {slice_ms:14.6f} {ratio:9.1f}x")
    print(f"  Calls per series: loops={loop_calls}, slices={slice_calls}")

print()
print("Both implementations produced identical arrays for each size.")
print("The ratio describes this task on this computer, not all NumPy operations.")
print("Rendering speed and FPS were not measured.")
