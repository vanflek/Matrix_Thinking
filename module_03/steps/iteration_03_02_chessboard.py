import pygame as pg

pg.init()

# Set the cell size and the board dimensions.
CELL = 80
ROWS = 8
COLS = 8

# Fit the window to the board.
width = COLS * CELL
height = ROWS * CELL
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Chessboard")

WHITE = (240, 240, 240)
BLACK = (30, 30, 30)

for row in range(ROWS):
    y = row * CELL

    for col in range(COLS):
        x = col * CELL

        # Choose a color for this cell.
        if (row + col) % 2 == 0:
            color = WHITE
        else:
            color = BLACK

        # Fill the entire cell.
        pg.draw.rect(screen, color, (x, y, CELL, CELL), 0)

# Show the completed board.
pg.display.update()

# Process pending events once, then keep the image visible.
pg.event.pump()
pg.time.wait(5000)
pg.quit()
