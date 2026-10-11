import pygame as pg
pg.init()
screen = pg.display.set_mode((800, 600))
screen.fill((0, 0, 0))

centers = [(200, 200), (400, 300), (600, 450)]
radius = 30
color = (255, 0, 0)
line_width = 3

for center in centers:
    pg.draw.circle(screen, color, center, radius, line_width)

pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
