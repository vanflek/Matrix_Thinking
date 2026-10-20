import numpy as np
import pygame as pg


def matrix_to_surface(matrix, cell_size):
    image = np.repeat(matrix, cell_size, axis=0)
    image = np.repeat(image, cell_size, axis=1)
    image = image.swapaxes(0, 1)

    return pg.surfarray.make_surface(image)


ROWS = 2
COLS = 3
CELL_SIZE = 32

BG_RGB = np.array([245, 245, 245], dtype=np.uint8)

matrix = np.zeros((ROWS, COLS, 3), dtype=np.uint8)
matrix[:] = BG_RGB
matrix[0, 0] = (255, 0, 0)

surface = matrix_to_surface(matrix, CELL_SIZE)

print(matrix.shape)
print(surface.get_size())
