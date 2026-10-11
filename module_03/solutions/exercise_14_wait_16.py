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
pg.display.set_caption("Chessboard with a while loop")

# Frame and board colors
FRAME = (140, 70, 20)
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)

# Draw the complete grid once
for row, y in enumerate(range(0, ROWS * CELL, CELL)):
    for col, x in enumerate(range(0, COLS * CELL, CELL)):

        # Reset the flag for each new cell
        is_border = False

        # Check whether the cell belongs to the frame
        if row == 0:
            is_border = True
        elif row == ROWS - 1:
            is_border = True
        elif col == 0:
            is_border = True
        elif col == COLS - 1:
            is_border = True

        # Use the saved result to choose a color
        if is_border:
            color = FRAME
        else:
            inner_row = row - 1
            inner_col = col - 1

            if (inner_row + inner_col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK

        # Draw the cell after choosing its color
        pg.draw.rect(screen, color, (x, y, CELL, CELL))

# Show the completed image
pg.display.update()

# Keep processing window events during the waiting loop
steps = 0
MAX_STEPS = 125

while steps < MAX_STEPS:
    pg.event.pump()
    pg.time.wait(16)
    steps += 1

pg.quit()
