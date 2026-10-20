import pygame as pg

pg.init()

# Two scalars describe the window size.
width = 800
height = 600
resolution = (width, height)
screen = pg.display.set_mode(resolution)

# Three components describe the background color.
bg_red = 0
bg_green = 0
bg_blue = 0
background = (bg_red, bg_green, bg_blue)

# Four scalars describe the position and size.
rect_x = 200
rect_y = 150
rect_width = 400
rect_height = 300

# Group the rectangle parameters in the expected order.
rect_pos_size = (rect_x, rect_y, rect_width, rect_height)

# Describe the rectangle's color and border thickness.
rect_color = (0, 180, 80)
rect_line_width = 0

# Fill the background, then draw the rectangle.
screen.fill(background)
pg.draw.rect(screen, rect_color, rect_pos_size, rect_line_width)

# Show the prepared image.
pg.display.update()

# Process pending events once, then pause.
pg.event.pump()
pg.time.wait(5000)

pg.quit()
