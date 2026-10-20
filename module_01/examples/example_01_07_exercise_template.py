import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

# --- your drawing code here ---


pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
