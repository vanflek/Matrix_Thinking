import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

circle_center = (width // 2, height // 2)

# Draw the large circle first.
pg.draw.circle(screen, (0, 200, 255), circle_center, 80, 0)

# Draw the small circle on top.
pg.draw.circle(screen, (255, 100, 100), circle_center, 40, 0)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
