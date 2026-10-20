import numpy as np

ROWS = 5
COLS = 7
LIGHT_RADIUS = 2

player = np.zeros((ROWS, COLS), dtype=np.uint8)
player[2, 3] = 1

pr, pc = np.argwhere(player == 1)[0]

Y, X = np.indices((ROWS, COLS))

dist2 = (Y - pr) ** 2 + (X - pc) ** 2

light = (
    dist2 <= LIGHT_RADIUS ** 2
).astype(np.uint8)

print("Distance squared:")
print(dist2)

print("Light mask:")
print(light)

print("Lit cells:", np.sum(light))

player.fill(0)
player[0, 0] = 1

pr, pc = np.argwhere(player == 1)[0]

dist2 = (Y - pr) ** 2 + (X - pc) ** 2
light = (
    dist2 <= LIGHT_RADIUS ** 2
).astype(np.uint8)

print(light)

Y_open, X_open = np.ogrid[:ROWS, :COLS]

dist2_open = (Y_open - pr) ** 2 + (X_open - pc) ** 2
light_open = (dist2_open <= LIGHT_RADIUS ** 2).astype(np.uint8)

print("Y shape:", Y_open.shape)
print("X shape:", X_open.shape)
print("Same distances:", np.array_equal(dist2_open, dist2))
print("Same mask:", np.array_equal(light_open, light))
