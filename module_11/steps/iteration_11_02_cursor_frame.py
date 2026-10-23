import numpy as np
import pygame as pg


def matrix_to_surface(matrix, cell_size):
    image = np.repeat(matrix, cell_size, axis=0)
    image = np.repeat(image, cell_size, axis=1)
    image = image.swapaxes(0, 1)

    return pg.surfarray.make_surface(image)


def build_grid_surface(rows, cols, cell_size, grid_color):
    width = cols * cell_size
    height = rows * cell_size
    grid_surface = pg.Surface((width, height), pg.SRCALPHA)

    for col in range(1, cols):
        x = col * cell_size
        pg.draw.line(grid_surface, grid_color,
                     (x, 0), (x, height - 1), 1)

    for row in range(1, rows):
        y = row * cell_size
        pg.draw.line(grid_surface, grid_color,
                     (0, y), (width - 1, y), 1)

    pg.draw.rect(grid_surface, grid_color,
                 (0, 0, width, height), 1)

    return grid_surface


pg.init()

ROWS = 32
COLS = 64
CELL_SIZE = 16
FPS = 60

BG_RGB = np.array([245, 245, 245], dtype=np.uint8)
GRID_COLOR = (185, 198, 206)
CURSOR_COLOR = (210, 90, 45)

matrix = np.zeros((ROWS, COLS, 3), dtype=np.uint8)
matrix[:] = BG_RGB

matrix[2:6, 3:7] = (255, 0, 0)
matrix[2:6, 9:13] = (0, 255, 0)
matrix[8:12, 3:7] = (0, 0, 255)

screen = pg.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pg.display.set_caption("Module 11 | RGB canvas")

grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
clock = pg.time.Clock()

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    frame_surface = matrix_to_surface(matrix, CELL_SIZE)
    screen.blit(frame_surface, (0, 0))
    screen.blit(grid_surface, (0, 0))

    if pg.mouse.get_focused():
        x_px, y_px = pg.mouse.get_pos()
        col = x_px // CELL_SIZE
        row = y_px // CELL_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            pg.draw.rect(
                screen,
                CURSOR_COLOR,
                (col * CELL_SIZE, row * CELL_SIZE,
                 CELL_SIZE, CELL_SIZE),
                2
            )

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
