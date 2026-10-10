import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

point_color = (255, 255, 0)
point_pos = (width // 2, height // 2)
screen.set_at(point_pos, point_color)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
