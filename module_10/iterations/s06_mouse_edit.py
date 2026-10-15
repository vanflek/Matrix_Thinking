import numpy as np
import pygame as pg


def life_calculation(matrix):
    rows, cols = matrix.shape
    new_matrix = np.zeros_like(matrix)

    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            block = matrix[y - 1:y + 2, x - 1:x + 2]
            alive_neighbors = int(np.sum(block)) - int(matrix[y, x])

            new_value = 0

            if matrix[y, x] == 1:
                if alive_neighbors == 2 or alive_neighbors == 3:
                    new_value = 1
            else:
                if alive_neighbors == 3:
                    new_value = 1

            new_matrix[y, x] = new_value

    return new_matrix


def matrix_to_surface(matrix, palette, cell_size):
    image = palette[matrix]
    image = np.repeat(image, cell_size, axis=0)
    image = np.repeat(image, cell_size, axis=1)

    return pg.surfarray.make_surface(image.swapaxes(0, 1))


pg.init()

ROWS = 15
COLS = 21
CELL_SIZE = 32
FPS = 60

COLORS = np.array([
    [245, 247, 250],
    [22, 139, 145],
], dtype=np.uint8)

matrix = np.zeros((ROWS, COLS), dtype=np.uint8)

# Place a horizontal blinker at the centre.
y = ROWS // 2
x = COLS // 2
matrix[y, x - 1:x + 2] = 1

screen = pg.display.set_mode((
    COLS * CELL_SIZE,
    ROWS * CELL_SIZE,
))
pg.display.set_caption("Game of Life | Space: next generation")

clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

            elif event.key == pg.K_SPACE:
                matrix = life_calculation(matrix)

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_px, y_px = event.pos
                x = x_px // CELL_SIZE
                y = y_px // CELL_SIZE

                if 1 <= y < ROWS - 1 and 1 <= x < COLS - 1:
                    matrix[y, x] = 1 - matrix[y, x]

    surface = matrix_to_surface(matrix, COLORS, CELL_SIZE)
    screen.blit(surface, (0, 0))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
