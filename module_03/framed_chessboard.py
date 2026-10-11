import pygame as pg

pg.init()

# Board size, including a one-cell frame on each side
CELL = 80
ROWS = 8 + 2
COLS = 8 + 2

# Window size follows the grid size
width = COLS * CELL
height = ROWS * CELL
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Chessboard with a frame")

# Frame and board colors
FRAME = (140, 70, 20)
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)

for row in range(ROWS):
    y = row * CELL

    for col in range(COLS):
        x = col * CELL

        # Choose the frame color for border cells
        if row == 0:
            color = FRAME
        elif row == ROWS - 1:
            color = FRAME
        elif col == 0:
            color = FRAME
        elif col == COLS - 1:
            color = FRAME
        else:
            # Choose a chessboard color for an inner cell
            inner_row = row - 1
            inner_col = col - 1

            if (inner_row + inner_col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK

        # Draw the cell after choosing its color
        pg.draw.rect(screen, color, (x, y, CELL, CELL))

pg.display.update()
pg.event.pump()
pg.time.wait(5000)
pg.quit()
