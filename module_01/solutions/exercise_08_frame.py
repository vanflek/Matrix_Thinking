import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

rect_color = (0, 255, 0)
rect_line_width = 5
rect_pos_size = (0, 0, width, height)

pg.draw.rect(screen, rect_color, rect_pos_size, rect_line_width)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
