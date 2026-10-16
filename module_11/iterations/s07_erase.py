import numpy as np
import pygame as pg


def matrix_to_surface(matrix, cell_size):
    image = np.repeat(matrix, cell_size, axis=0)
    image = np.repeat(image, cell_size, axis=1)
    image = image.swapaxes(0, 1)

    return pg.surfarray.make_surface(image)


def build_grid_surface(rows, cols, cell_size, grid_color):
    width = cols * cell_size
    height = rows * cell_size
    grid_surface = pg.Surface((width, height), pg.SRCALPHA)

    for col in range(1, cols):
        x = col * cell_size
        pg.draw.line(grid_surface, grid_color,
                     (x, 0), (x, height - 1))

    for row in range(1, rows):
        y = row * cell_size
        pg.draw.line(grid_surface, grid_color,
                     (0, y), (width - 1, y))

    pg.draw.rect(grid_surface, grid_color,
                 (0, 0, width, height), 1)

    return grid_surface


def handle_controls(events, state, cell_size):
    state["paint_cells"] = []
    state["erase"] = (pg.key.get_mods() & pg.KMOD_SHIFT) != 0

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                state["channel"] = 0
            elif event.key == pg.K_g:
                state["channel"] = 1
            elif event.key == pg.K_b:
                state["channel"] = 2

        elif event.type == pg.MOUSEWHEEL:
            channel = state["channel"]
            value = int(state["brush_rgb"][channel])
            value = value + event.y * 5
            value = max(0, min(255, value))
            state["brush_rgb"][channel] = value

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_px, y_px = event.pos
                col = x_px // cell_size
                row = y_px // cell_size
                state["paint_cells"].append((row, col))


    left_down = pg.mouse.get_pressed()[0]

    if left_down and pg.mouse.get_focused():
        x_px, y_px = pg.mouse.get_pos()
        col = x_px // cell_size
        row = y_px // cell_size
        state["paint_cells"].append((row, col))


def apply_actions(matrix, state, bg_rgb):
    rows, cols = matrix.shape[:2]

    if state["erase"]:
        color = bg_rgb
    else:
        color = state["brush_rgb"]

    for row, col in state["paint_cells"]:
        if 0 <= row < rows and 0 <= col < cols:
            matrix[row, col] = color


pg.init()

ROWS = 32
COLS = 64
CELL_SIZE = 16
FPS = 60

BG_RGB = np.array([245, 245, 245], dtype=np.uint8)
GRID_COLOR = (185, 198, 206)

matrix = np.zeros((ROWS, COLS, 3), dtype=np.uint8)
matrix[:] = BG_RGB

matrix[2:6, 3:7] = (255, 0, 0)
matrix[2:6, 9:13] = (0, 255, 0)
matrix[8:12, 3:7] = (0, 0, 255)

screen = pg.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pg.display.set_caption("Module 11 | RGB canvas")

grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
clock = pg.time.Clock()

state = {
    "cell": (0, 0),  # (row, col)
    "inside": False,
    "brush_rgb": np.array([0, 0, 0], dtype=np.uint8),
    "channel": 0,
    "paint_cells": [],
    "erase": False,
}

running = True

while running:
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    handle_controls(events, state, CELL_SIZE)
    apply_actions(matrix, state, BG_RGB)

    r, g, b = state["brush_rgb"]
    channel = state["channel"]
    pg.display.set_caption(
        f"Module 11 | R={r} G={g} B={b} | channel={channel}"
    )

    frame_surface = matrix_to_surface(matrix, CELL_SIZE)
    screen.blit(frame_surface, (0, 0))
    screen.blit(grid_surface, (0, 0))

    state["inside"] = False

    if pg.mouse.get_focused():
        x_px, y_px = pg.mouse.get_pos()
        col = x_px // CELL_SIZE
        row = y_px // CELL_SIZE

        state["cell"] = (row, col)
        state["inside"] = (
            0 <= row < ROWS and 0 <= col < COLS
        )

    if state["inside"]:
        row, col = state["cell"]
        r, g, b = state["brush_rgb"]
        brush_color = (int(r), int(g), int(b))

        pg.draw.rect(
            screen,
            brush_color,
            (col * CELL_SIZE, row * CELL_SIZE,
             CELL_SIZE, CELL_SIZE),
            2
        )

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
