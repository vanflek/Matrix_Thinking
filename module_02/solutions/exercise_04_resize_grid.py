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
CELL = 60
ROWS = 6
COLS = 10

# Describe the pixel coordinates of row and column starts.
row_positions = range(0, ROWS * CELL, CELL)
col_positions = range(0, COLS * CELL, CELL)

# Prepare one font for all labels.
font = pg.font.SysFont("Arial", 20)
screen.fill(BACKGROUND)

for row, y in enumerate(row_positions):
    for col, x in enumerate(col_positions):
        # Draw the cell outline with a two-pixel inset.
        rect = (x + 2, y + 2, CELL - 4, CELL - 4)
        pg.draw.rect(screen, CELL_COLOR, rect, 2)

        # Create and place the label with the cell address.
        text = f"({row}, {col})"
        label = font.render(text, True, TEXT_COLOR)
        screen.blit(label, (x + 10, y + 8))

# Show the completed grid.
pg.display.update()

# Process pending events once, then keep the image visible.
pg.event.pump()
pg.time.wait(5000)
pg.quit()
