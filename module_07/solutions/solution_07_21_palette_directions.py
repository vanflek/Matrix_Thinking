# Practice 21: palette directions.
import pygame as pg
import numpy as np

pg.init()

# Set the grid size and frame rate limit.
ROWS = 16
COLS = 16
CELL_SIZE = 40
FPS = 60

width = COLS * CELL_SIZE
height = ROWS * CELL_SIZE

screen = pg.display.set_mode((width, height))
pg.display.set_caption("Pixel Art Editor - arrows + space")
clock = pg.time.Clock()

# Each palette row stores one RGB color.
COLORS = np.array([
    [245, 245, 245],  # 0: background
    [30, 30, 30],     # 1: black
    [220, 60, 60],    # 2: red
    [60, 120, 220],   # 3: blue
    [60, 180, 90],    # 4: green
    [240, 200, 60],   # 5: yellow
    [200, 90, 220],   # 6: purple
    [60, 200, 200],   # 7: cyan
    [240, 140, 60],   # 8: orange
    [160, 160, 160],  # 9: gray
], dtype=np.uint8)

GRID_COLOR = (180, 180, 180)
CURSOR_COLOR = (255, 50, 200)

# Store color indices in the canvas and (row, column) in the cursor.
matrix = np.zeros((ROWS, COLS), dtype=np.int16)
cursor = np.array([0, 0], dtype=np.int16)
current_color = 1
brush = 1

save_png = False

show_info = False
font = pg.font.SysFont("Arial", 20)

running = True
while running:
    # Update the data in response to events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

            # Move the cursor and wrap around the grid edges.
            elif event.key == pg.K_LEFT:
                cursor[1] = (cursor[1] - 1) % COLS
            elif event.key == pg.K_RIGHT:
                cursor[1] = (cursor[1] + 1) % COLS
            elif event.key == pg.K_UP:
                cursor[0] = (cursor[0] - 1) % ROWS
            elif event.key == pg.K_DOWN:
                cursor[0] = (cursor[0] + 1) % ROWS

            # Select a color in either direction, then paint the brush area.
            elif event.key == pg.K_SPACE:
                mods = event.mod
                if mods & pg.KMOD_SHIFT:
                    current_color = (current_color - 1) % len(COLORS)
                else:
                    current_color = (current_color + 1) % len(COLORS)
                row = int(cursor[0])
                col = int(cursor[1])

                row_start = max(0, row - brush)
                row_stop = min(ROWS, row + brush + 1)
                col_start = max(0, col - brush)
                col_stop = min(COLS, col + brush + 1)

                matrix[row_start:row_stop, col_start:col_stop] = current_color

            elif event.key == pg.K_s:
                np.save("art.npy", matrix)

            elif event.key == pg.K_l:
                try:
                    matrix = np.load("art.npy")
                except FileNotFoundError:
                    pass

            elif event.key == pg.K_p:
                save_png = True

            elif event.key == pg.K_i:
                show_info = not show_info

    # Draw each cell using its color index and the palette.
    for row in range(ROWS):
        for col in range(COLS):
            color_index = matrix[row, col]
            rgb = COLORS[color_index]
            color = (int(rgb[0]), int(rgb[1]), int(rgb[2]))

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            pg.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), 0)
            pg.draw.rect(
                screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1
            )

    if save_png:
        pg.image.save(screen, "art.png")
        save_png = False

    # Draw the cursor over the image without changing the matrix.
    cursor_x = int(cursor[1]) * CELL_SIZE
    cursor_y = int(cursor[0]) * CELL_SIZE

    pg.draw.rect(
        screen,
        CURSOR_COLOR,
        (cursor_x + 2, cursor_y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
        3
    )

    if show_info:
        row = int(cursor[0])
        col = int(cursor[1])
        cell_index = int(matrix[row, col])
        text = f"cursor=({row},{col})  cell={cell_index}  current={current_color}"
        label = font.render(text, True, (20, 20, 20), (245, 245, 245))
        screen.blit(label, (10, 10))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
