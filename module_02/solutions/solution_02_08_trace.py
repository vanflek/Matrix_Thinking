import pygame as pg

pg.init()

# Create the window.
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Grid with enumerate")

# Set the colors.
BACKGROUND = (230, 230, 230)
CELL_COLOR = (180, 80, 50)
TEXT_COLOR = (20, 20, 20)

# Set the cell size and the number of rows and columns.
CELL = 80
ROWS = 5
COLS = 8

# Describe the pixel coordinates of row and column starts.
row_positions = range(0, ROWS * CELL, CELL)
col_positions = range(0, COLS * CELL, CELL)

screen.fill(BACKGROUND)

for row, y in enumerate(row_positions):
    for col, x in enumerate(col_positions):
        # Draw the cell outline with a two-pixel inset.
        rect = (x + 2, y + 2, CELL - 4, CELL - 4)
        pg.draw.rect(screen, CELL_COLOR, rect, 2)

        print(f"cell ({row}, {col}) at pixels ({x}, {y})")

# Show the completed grid.
pg.display.update()

# Process pending events once, then keep the image visible.
pg.event.pump()
pg.time.wait(5000)
pg.quit()
