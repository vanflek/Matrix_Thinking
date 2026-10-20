import pygame as pg

pg.init()

# Create the window.
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Brick wall")

# The background remains visible in the gaps.
BACKGROUND = (200, 200, 200)
BRICK = (180, 80, 50)
TEXT_COLOR = (20, 20, 20)

# Prepare one font for all labels.
font = pg.font.SysFont("Arial", 20)

# Set the cell size and count the complete cells.
BRICK_WIDTH = 100
BRICK_HEIGHT = 40
ROWS = height // BRICK_HEIGHT
COLS = width // BRICK_WIDTH

screen.fill(BACKGROUND)

# Draw every column in each row.
for row in range(ROWS):
    y = row * BRICK_HEIGHT
    for col in range(COLS):
        x = col * BRICK_WIDTH

        # Leave a two-pixel inset on each side of the cell.
        rect = (
            x + 2,
            y + 2,
            BRICK_WIDTH - 4,
            BRICK_HEIGHT - 4
        )
        pg.draw.rect(screen, BRICK, rect)

        # Place the label after drawing its background.
        text = f"({row}, {col})"
        label = font.render(text, True, TEXT_COLOR)
        screen.blit(label, (x + 10, y + 8))

# Show the completed wall.
pg.display.update()

# Process pending events once, then keep the image visible.
pg.event.pump()
pg.time.wait(5000)
pg.quit()
