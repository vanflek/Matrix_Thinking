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

# Calculate the center from the window dimensions.
center_x = width // 2
center_y = height // 2
circle_center = (center_x, center_y)

# Describe the circle with scalars and a color vector.
circle_radius = 80
circle_color = (0, 200, 255)
circle_width = 0

# Fill the background, then draw the circle.
screen.fill(background)
pg.draw.circle(screen, circle_color, circle_center, circle_radius, circle_width)

# Show the prepared image.
pg.display.update()

# Process pending events once, then pause.
pg.event.pump()
pg.time.wait(5000)

pg.quit()
