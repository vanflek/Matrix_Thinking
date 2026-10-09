import pygame as pg
pg.init()

# Set the window size in pixels.
width = 800
height = 600
resolution = (width, height)
screen = pg.display.set_mode(resolution)

title = "Module 0 - A living window"
pg.display.set_caption(title)

background1 = (0, 255, 0)  # Green
background2 = (0, 0, 255)  # Blue

screen.fill(background1)
pg.display.update()
pg.event.pump()
pg.time.wait(1000)

screen.fill(background2)
pg.display.update()
pg.event.pump()
pg.time.wait(2000)

pg.quit()
