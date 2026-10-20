# The outside border follows the last visible pixels.
import numpy as np
import pygame as pg

COLORS = np.array([
    [245, 245, 245], [0, 0, 0], [255, 255, 255],
    [255, 0, 0], [0, 255, 0], [0, 0, 255],
], dtype=np.uint8)
def matrix_to_surface(matrix, palette, cell_size):
    rgb_small = palette[matrix]

    rgb_rows = np.repeat(rgb_small, cell_size, axis=0)
    rgb_big = np.repeat(rgb_rows, cell_size, axis=1)

    rgb_for_pygame = np.swapaxes(rgb_big, 0, 1)
    image = pg.surfarray.make_surface(rgb_for_pygame)

    return image

matrix = np.array([[0, 3, 0], [5, 0, 3]], dtype=np.uint8)
CELL_SIZE = 40
pg.init()
field_surface = matrix_to_surface(matrix, COLORS, CELL_SIZE)
print(field_surface.get_size())
rows, cols = matrix.shape
cell_size = CELL_SIZE
width = cols * cell_size
height = rows * cell_size
grid_color = (80, 80, 80)
grid_surface = pg.Surface((width, height), pg.SRCALPHA)
grid_surface.fill((0, 0, 0, 0))
for col in range(1, cols):
    x = col * cell_size
    pg.draw.line(grid_surface, grid_color, (x, 0), (x, height - 1))
for row in range(1, rows):
    y = row * cell_size
    pg.draw.line(grid_surface, grid_color, (0, y), (width - 1, y))
pg.draw.rect(grid_surface, grid_color, (0, 0, width, height), 1)

screen = pg.display.set_mode(field_surface.get_size())
pg.display.set_caption("Collector - step preview")
clock = pg.time.Clock()
screen.blit(field_surface, (0, 0))
screen.blit(grid_surface, (0, 0))
pg.display.flip()

# Keep the preview open until Esc or the window close button is pressed.
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    clock.tick(60)

pg.quit()
