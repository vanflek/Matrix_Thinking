import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

line_color = (255, 255, 0)
line_width = 3
center_x = width // 2
center_y = height // 2

horizontal_start = (0, center_y)
horizontal_end = (width - 1, center_y)
vertical_start = (center_x, 0)
vertical_end = (center_x, height - 1)

pg.draw.line(screen, line_color, horizontal_start, horizontal_end, line_width)
pg.draw.line(screen, line_color, vertical_start, vertical_end, line_width)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
