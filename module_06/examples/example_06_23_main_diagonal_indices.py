import pygame as pg
import numpy as np

pg.init()

# Display settings: cell size in pixels and frame rate limit.
CELL_SIZE = 40
FPS = 60

# RGB colors used to display the matrix.
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
GRID = (180, 180, 180)
BG = (230, 230, 230)

# Create the data: 0 means a light cell, 1 means a dark cell.
matrix = np.zeros((16, 16), dtype=np.uint8)
ROWS, COLS = matrix.shape

# --- PATTERN START ---
matrix[:, :] = 0
indices = np.arange(ROWS)
matrix[indices, indices] = 1
print(matrix)
# --- PATTERN END ---

# Each matrix element occupies a CELL_SIZE x CELL_SIZE square.
width = COLS * CELL_SIZE
height = ROWS * CELL_SIZE

screen = pg.display.set_mode((width, height))
pg.display.set_caption("Main diagonal indices")
clock = pg.time.Clock()

running = True
while running:
    clock.tick(FPS)

    # Process window events and keyboard presses.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    screen.fill(BG)

    # Visit every matrix element: row first, then column.
    for row in range(ROWS):
        for col in range(COLS):
            value = matrix[row, col]

            # Select a color using the stored value.
            if value == 1:
                color = BLACK
            else:
                color = WHITE

            # Convert the column to x and the row to y.
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # Draw the filled cell and its one-pixel border.
            pg.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pg.draw.rect(screen, GRID, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # Show the completed frame.
    pg.display.flip()

pg.quit()
