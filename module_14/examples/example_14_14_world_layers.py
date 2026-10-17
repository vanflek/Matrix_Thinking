import numpy as np

ROWS = 3
COLS = 5

LAYER_PLAYER = 0
LAYER_BUG = 1
LAYERS = 2

world = np.zeros(
    (ROWS, COLS, LAYERS),
    dtype=np.uint8
)

world[1, 2, LAYER_PLAYER] = 1
world[1, 4, LAYER_BUG] = 1

assert world[:, :, LAYER_PLAYER].sum() == 1
assert world[:, :, LAYER_BUG].sum() == 1

print("World shape:", world.shape)

print("Player:")
print(world[:, :, LAYER_PLAYER])

print("Bug:")
print(world[:, :, LAYER_BUG])

world[:, :, LAYER_PLAYER].fill(0)
world[1, 4, LAYER_PLAYER] = 1

print("Cell contents:", world[1, 4])

overlap = (
    world[:, :, LAYER_PLAYER]
    * world[:, :, LAYER_BUG]
)

print("Any overlap:", overlap.any())
