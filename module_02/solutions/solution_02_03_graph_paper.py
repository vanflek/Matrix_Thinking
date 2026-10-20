import pygame as pg

pg.init()
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Graph paper")
screen.fill((0, 0, 0))

STEP = 40
LINE_COLOR = (80, 80, 80)

# Draw each family of lines with its own loop.
for x in range(0, width, STEP):
    pg.draw.line(screen, LINE_COLOR, (x, 0), (x, height - 1))

for y in range(0, height, STEP):
    pg.draw.line(screen, LINE_COLOR, (0, y), (width - 1, y))

pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
