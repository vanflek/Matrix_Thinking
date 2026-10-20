import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

pole_rect = (100, 150, 10, 300)
flag_rect = (110, 160, 250, 150)
top_stripe = (110, 160, 250, 50)
bottom_stripe = (110, 260, 250, 50)

# Draw the pole and the white flag.
pg.draw.rect(screen, (150, 150, 150), pole_rect, 0)
pg.draw.rect(screen, (255, 255, 255), flag_rect, 0)

# Leave the middle stripe white.
pg.draw.rect(screen, (255, 0, 0), top_stripe, 0)
pg.draw.rect(screen, (0, 0, 255), bottom_stripe, 0)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
