import numpy as np
import pygame as pg



def get_gray(pixels):
    width, height = pixels.shape[:2]
    gray = np.zeros((width, height), dtype=float)

    for x in range(width):
        for y in range(height):
            red, green, blue = pixels[x, y]

            gray[x, y] = (
                0.299 * red
                + 0.587 * green
                + 0.114 * blue
            )

    return gray


pg.init()

image = pg.image.load("cat.png")
pixels = pg.surfarray.array3d(image)
gray = get_gray(pixels)
gray_rgb = np.zeros_like(pixels)
for x in range(gray.shape[0]):
    for y in range(gray.shape[1]):
        value = gray[x, y]
        gray_rgb[x, y] = (value, value, value)
surface = pg.surfarray.make_surface(gray_rgb)

screen = pg.display.set_mode(surface.get_size())
pg.display.set_caption("ASCII learning step B01")
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
