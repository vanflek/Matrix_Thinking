import numpy as np
import pygame as pg



def get_gray(pixels):
    return (
        0.299 * pixels[:, :, 0]
        + 0.587 * pixels[:, :, 1]
        + 0.114 * pixels[:, :, 2]
    )


pg.init()

image = pg.image.load("cat.png")
pixels = pg.surfarray.array3d(image)
gray = get_gray(pixels)
gray_rgb = np.repeat(gray[:, :, np.newaxis], 3, axis=2)
surface = pg.surfarray.make_surface(gray_rgb.astype(np.uint8))

screen = pg.display.set_mode(surface.get_size())
pg.display.set_caption("ASCII learning step B02")
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
