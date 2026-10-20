import pygame as pg

pg.init()

# Create the window.
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Circles with a for loop")

# Set the background and circle color.
background = (0, 0, 0)
color = (255, 0, 0)

# All circles share a center and an outline width.
center = (width // 2, height // 2)
line_width = 10

# Prepare the background once, then draw all five circles.
screen.fill(background)
for radius in range(200, 0, -40):
    pg.draw.circle(screen, color, center, radius, line_width)

# Show the completed image after the loop finishes.
pg.display.update()

# Process pending events once, then keep the image visible.
pg.event.pump()
pg.time.wait(5000)

pg.quit()
