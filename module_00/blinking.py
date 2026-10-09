import pygame as pg
pg.init()

# Set the window size in pixels.
width = 800
height = 600
resolution = (width, height)
screen = pg.display.set_mode(resolution)

title = "Module 0 - A living window"
pg.display.set_caption(title)

green_color = (0, 255, 0)
black_color = (0, 0, 0)
pause = 200

screen.fill(green_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(black_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(green_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(black_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(green_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(black_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(green_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(black_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(green_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

screen.fill(black_color)
pg.display.update()
pg.event.pump()
pg.time.wait(pause)

pg.quit()
