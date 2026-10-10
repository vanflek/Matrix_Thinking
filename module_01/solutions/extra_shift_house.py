import pygame as pg
pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

background = (0, 0, 0)
screen.fill(background)

shift_x = 50
wall_rect = (250 + shift_x, 250, 300, 200)
door_rect = (370 + shift_x, 320, 60, 130)
left_window_rect = (280 + shift_x, 270, 60, 50)
right_window_rect = (460 + shift_x, 270, 60, 50)


# Draw the walls before the door and windows.
pg.draw.rect(screen, (150, 75, 0), wall_rect, 0)
pg.draw.rect(screen, (100, 50, 0), door_rect, 0)
pg.draw.rect(screen, (200, 200, 255), left_window_rect, 0)
pg.draw.rect(screen, (200, 200, 255), right_window_rect, 0)

# Draw the ground directly below the house.
pg.draw.line(screen, (0, 255, 0), (0, 450), (width - 1, 450), 1)



pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
