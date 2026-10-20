import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

center_x = width // 2
center_y = height // 2
center = (center_x, center_y)
arm_length = 150
color = (255, 255, 255)
line_width = 3

horizontal_start = (center_x - arm_length, center_y)
horizontal_end = (center_x + arm_length, center_y)
vertical_start = (center_x, center_y - arm_length)
vertical_end = (center_x, center_y + arm_length)

pg.draw.line(screen, color, horizontal_start, horizontal_end, line_width)
pg.draw.line(screen, color, vertical_start, vertical_end, line_width)

# Draw outlines so that the lines remain visible.
pg.draw.circle(screen, color, center, 40, line_width)
pg.draw.circle(screen, color, center, 80, line_width)
pg.draw.circle(screen, color, center, 120, line_width)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
