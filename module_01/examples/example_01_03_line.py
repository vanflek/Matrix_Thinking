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

# Four scalars describe the two endpoints.
start_x = 100
start_y = 100
end_x = 700
end_y = 500

# Group the coordinates into two position vectors.
start_pos = (start_x, start_y)
end_pos = (end_x, end_y)

# Describe the line's color and thickness.
line_color = (255, 255, 0)
line_width = 5

# Fill the background, then connect the endpoints.
screen.fill(background)
pg.draw.line(screen, line_color, start_pos, end_pos, line_width)

# Show the prepared image.
pg.display.update()

# Process pending events once, then pause.
pg.event.pump()
pg.time.wait(5000)

pg.quit()
