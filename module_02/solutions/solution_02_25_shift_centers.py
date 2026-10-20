import pygame as pg
pg.init()
screen = pg.display.set_mode((800, 600))
screen.fill((0, 0, 0))
radius = 30
color = (255, 0, 0)
line_width = 3

centers = [(200, 200), (400, 300), (600, 450)]

for x, y in centers:
    new_center = (x + 50, y)
    print(new_center)
    pg.draw.circle(screen, color, new_center, radius, line_width)

pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
