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

assert Cx_left.shape == (COLS, COLS)
assert Cx_right.shape == (COLS, COLS)

assert Cy_up.shape == (ROWS, ROWS)
assert Cy_down.shape == (ROWS, ROWS)

print("Shape checks passed")

operators = (Cx_left, Cx_right, Cy_up, Cy_down)

for operator in operators:
    assert np.all((operator == 0) | (operator == 1))
    assert np.all(operator.sum(axis=0) == 1)
    assert np.all(operator.sum(axis=1) == 1)

print("Permutation checks passed")

for row in range(ROWS):
    for col in range(COLS):
        probe = np.zeros((ROWS, COLS), dtype=np.uint8)
        probe[row, col] = 1

        assert np.array_equal(
            probe @ Cx_right,
            np.roll(probe, 1, axis=1)
        )

        assert np.array_equal(
            probe @ Cx_left,
            np.roll(probe, -1, axis=1)
        )

        assert np.array_equal(
            Cy_down @ probe,
            np.roll(probe, 1, axis=0)
        )

        assert np.array_equal(
            Cy_up @ probe,
            np.roll(probe, -1, axis=0)
        )

print("Movement checks passed")

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
