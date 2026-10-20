import pygame as pg

pg.init()

# Two scalars describe the window size.
width = 800
height = 600
resolution = (width, height)
screen = pg.display.set_mode(resolution)

# Three components describe the background color.
red = 0
green = 0
blue = 0
background = (red, green, blue)

# Coordinates describe the pixel's position.
point_x = 100
point_y = 100

# RGB components describe the pixel's color.
point_color = (255, 255, 255)

# Prepare the background, then change one pixel.
screen.fill(background)
screen.set_at((point_x, point_y), point_color)

# Show the prepared image.
pg.display.update()

# Process pending events once, then pause.
pg.event.pump()
pg.time.wait(5000)

pg.quit()
