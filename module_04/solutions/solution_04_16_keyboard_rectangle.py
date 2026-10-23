# Move a rectangle by discrete key presses and keep it inside the window.
import pygame as pg

pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Rectangle control - arrow keys and Esc")

BACKGROUND = (230, 230, 230)
BLUE = (60, 120, 200)
FPS = 60
clock = pg.time.Clock()

rect_width = 120
rect_height = 80
step = 40

# These coordinates describe the top-left corner, not the center.
x = width // 2 - rect_width // 2
y = height // 2 - rect_height // 2
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_LEFT:
                x = x - step
            elif event.key == pg.K_RIGHT:
                x = x + step
            elif event.key == pg.K_UP:
                y = y - step
            elif event.key == pg.K_DOWN:
                y = y + step

    clock.tick(FPS)

    # A rectangle is described by its corner and two dimensions.
    if x < 0:
        x = 0
    elif x + rect_width > width:
        x = width - rect_width

    if y < 0:
        y = 0
    elif y + rect_height > height:
        y = height - rect_height

    screen.fill(BACKGROUND)
    pg.draw.rect(screen, BLUE, (x, y, rect_width, rect_height), 0)
    pg.display.flip()

pg.quit()
