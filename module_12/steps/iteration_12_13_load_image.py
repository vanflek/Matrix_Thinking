import numpy as np
import pygame as pg






pg.init()

image = pg.image.load("cat.png")
pixels = pg.surfarray.array3d(image)
print("Image array shape (X, Y, RGB):", pixels.shape)
print("Pixel data type:", pixels.dtype)
surface = pg.surfarray.make_surface(pixels)

screen = pg.display.set_mode(surface.get_size())
pg.display.set_caption("ASCII learning step B00")
clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    if running:
        screen.blit(surface, (0, 0))
        pg.display.flip()
    clock.tick(60)
pg.quit()
