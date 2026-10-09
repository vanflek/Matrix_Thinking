import pygame as pg
pg.init()

# Set the window size in pixels.
width = 800
height = 600
resolution = (width, height)
screen = pg.display.set_mode(resolution)

title = "Module 0 - A living window"
pg.display.set_caption(title)

# Set the red, green and blue channels.
red = 0
green = 255
blue = 0
background = (red, green, blue)

# Fill the display surface and show the frame.
screen.fill(background)
pg.display.update()

# Process pending system events once, then pause.
pg.event.pump()
pg.time.wait(3000)

pg.quit()
