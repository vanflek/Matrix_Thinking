import numpy as np
import pygame as pg

COLORS = np.array([
    [245, 245, 245], [0, 0, 0], [255, 255, 255],
    [255, 0, 0], [0, 255, 0], [0, 0, 255],
], dtype=np.uint8)

# Integer indices can select the same palette row more than once.
indices = np.array([3, 0, 3, 5, 0])
print("Selected RGB vectors:")
print(COLORS[indices])

matrix = np.array([[0, 3, 0], [5, 0, 3]])
rgb_small = COLORS[matrix]
CELL_SIZE = 2
rgb_rows = np.repeat(rgb_small, CELL_SIZE, axis=0)
rgb_big = np.repeat(rgb_rows, CELL_SIZE, axis=1)
rgb_for_pygame = np.swapaxes(rgb_big, 0, 1)
print("RGB array:", rgb_small.shape)
print("Repeated rows:", rgb_rows.shape)
print("Repeated columns:", rgb_big.shape)
print("Pygame axis order:", rgb_for_pygame.shape)

# A Surface can be prepared without opening a display window.
pg.init()
image = pg.surfarray.make_surface(rgb_for_pygame)
print("Surface width and height:", image.get_size())
pg.quit()
