import pygame as pg

pg.init()

# Create the window.
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Staggered brick wall")

# The background remains visible in the gaps.
BACKGROUND = (200, 200, 200)
BRICK = (180, 80, 50)

BRICK_WIDTH = 100
BRICK_HEIGHT = 40
ROWS = height // BRICK_HEIGHT
COLS = width // BRICK_WIDTH + 1

screen.fill(BACKGROUND)

for row in range(ROWS):
    y = row * BRICK_HEIGHT

    # Choose the starting position once for this row.
    if row % 2 == 0:
        x_start = 0
    else:
        x_start = -(BRICK_WIDTH // 2)

    for col in range(COLS):
        x = x_start + col * BRICK_WIDTH

        # Leave a two-pixel inset on each side of the cell.
        rect = (
            x + 2,
            y + 2,
            BRICK_WIDTH - 4,
            BRICK_HEIGHT - 4
        )
        pg.draw.rect(screen, BRICK, rect)

# Show the completed wall.
pg.display.update()

# Process pending events once, then keep the image visible.
pg.event.pump()
pg.time.wait(5000)
pg.quit()
