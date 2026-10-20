import numpy as np
import pygame as pg

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
])
print(matrix)

pg.init()
screen = pg.display.set_mode((600, 400))
pg.display.set_caption("NumPy and Pygame work!")
screen.fill((40, 100, 160))
pg.display.flip()

clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    clock.tick(30)

pg.quit()
