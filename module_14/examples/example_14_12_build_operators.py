import numpy as np


def build_shift_operators(cols, rows):
    Cx_right = np.zeros((cols, cols), dtype=np.uint8)
    j = np.arange(cols)
    Cx_right[j, (j + 1) % cols] = 1

    Cy_down = np.zeros((rows, rows), dtype=np.uint8)
    i = np.arange(rows)
    Cy_down[(i + 1) % rows, i] = 1

    Cx_left = Cx_right.T
    Cy_up = Cy_down.T

    return Cx_left, Cx_right, Cy_up, Cy_down


ROWS = 3
COLS = 5

Cx_left, Cx_right, Cy_up, Cy_down = build_shift_operators(
    COLS, ROWS
)

P = np.zeros((ROWS, COLS), dtype=np.uint8)
P[1, 2] = 1

print("Right:")
print(P @ Cx_right)

print("Left:")
print(P @ Cx_left)

print("Down:")
print(Cy_down @ P)

print("Up:")
print(Cy_up @ P)
