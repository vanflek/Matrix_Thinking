import numpy as np
import pygame as pg

WIDTH = 640
HEIGHT = 480
CELL_SIZE = 40

radius = 160.0
angles_degrees = np.arange(0.0, 360.0, 5.0)
angles_radians = np.deg2rad(angles_degrees)

x_values = radius * np.cos(angles_radians)
y_values = radius * np.sin(angles_radians)
points = np.column_stack((x_values, y_values))

screen_points = np.column_stack((
    WIDTH / 2 + points[:, 0],
    HEIGHT / 2 - points[:, 1],
))

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Circle from points")
clock = pg.time.Clock()

screen.fill((250, 250, 250))

for x in range(0, WIDTH, CELL_SIZE):
    pg.draw.line(screen, (225, 230, 235), (x, 0), (x, HEIGHT - 1))
for y in range(0, HEIGHT, CELL_SIZE):
    pg.draw.line(screen, (225, 230, 235), (0, y), (WIDTH - 1, y))

pg.draw.line(screen, (110, 120, 130), (0, HEIGHT // 2), (WIDTH - 1, HEIGHT // 2), 2)
pg.draw.line(screen, (110, 120, 130), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT - 1), 2)
pg.draw.lines(screen, (0, 130, 155), True, screen_points, 2)

for point in screen_points:
    pg.draw.circle(screen, (200, 65, 55), point, 3)

pg.display.flip()

running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

pg.quit()
