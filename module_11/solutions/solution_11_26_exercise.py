import numpy as np
import pygame as pg


# Prepare the image without changing the cell data.
def matrix_to_surface(matrix, cell_size):
    image = np.repeat(matrix, cell_size, axis=0)
    image = np.repeat(image, cell_size, axis=1)
    image = image.swapaxes(0, 1)

    return pg.surfarray.make_surface(image)


# Build the transparent grid once.
def build_grid_surface(rows, cols, cell_size, grid_color):
    width = cols * cell_size
    height = rows * cell_size
    grid_surface = pg.Surface((width, height), pg.SRCALPHA)

    for col in range(1, cols):
        x = col * cell_size
        pg.draw.line(grid_surface, grid_color,
                     (x, 0), (x, height - 1), 1)

    for row in range(1, rows):
        y = row * cell_size
        pg.draw.line(grid_surface, grid_color,
                     (0, y), (width - 1, y), 1)

    pg.draw.rect(grid_surface, grid_color,
                 (0, 0, width, height), 1)

    return grid_surface


# Turn input into commands for the current frame.
def handle_controls(events, state, cell_size):
    state["clear"] = False
    state["save"] = False
    state["load"] = False
    state["export"] = False
    state["paint_cells"] = []
    state["pipette_cells"] = []
    state["erase"] = (pg.key.get_mods() & pg.KMOD_SHIFT) != 0

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                state["channel"] = 0
            elif event.key == pg.K_g:
                state["channel"] = 1
            elif event.key == pg.K_b:
                state["channel"] = 2
            elif event.key == pg.K_c:
                state["clear"] = True
            elif event.key == pg.K_s:
                state["save"] = True
            elif event.key == pg.K_l:
                state["load"] = True
            elif event.key == pg.K_p:
                state["export"] = True

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

            elif event.button == 3:
                x_px, y_px = event.pos
                col = x_px // cell_size
                row = y_px // cell_size
                state["pipette_cells"].append((row, col))

    left_down = pg.mouse.get_pressed()[0]

    if left_down and pg.mouse.get_focused():
        x_px, y_px = pg.mouse.get_pos()
        col = x_px // cell_size
        row = y_px // cell_size
        state["paint_cells"].append((row, col))


# Priority: clear, then pipette, then paint or erase.
def apply_actions(matrix, state, bg_rgb):
    if state["clear"]:
        matrix[:] = bg_rgb
        return

    rows, cols = matrix.shape[:2]

    if state["pipette_cells"]:
        for row, col in state["pipette_cells"]:
            if 0 <= row < rows and 0 <= col < cols:
                state["brush_rgb"][:] = matrix[row, col]
        return

    if state["erase"]:
        color = bg_rgb
    else:
        color = state["brush_rgb"]

    for row, col in state["paint_cells"]:
        if 0 <= row < rows and 0 <= col < cols:
            matrix[row, col] = color


def save_matrix_npy(matrix, filename):
    try:
        np.save(filename, matrix)
    except OSError:
        print("Could not save:", filename)
        return

    print("Saved:", filename)


def load_matrix_npy(filename, expected_shape, expected_dtype):
    try:
        loaded = np.load(filename, allow_pickle=False)
    except FileNotFoundError:
        print("File not found:", filename)
        return None
    except (OSError, ValueError, EOFError):
        print("Could not read:", filename)
        return None

    if not isinstance(loaded, np.ndarray):
        loaded.close()
        print("Expected a single array in an NPY file.")
        return None

    if loaded.shape != expected_shape:
        print("The array has the wrong shape.")
        return None

    if loaded.dtype != expected_dtype:
        print("The array has the wrong data type.")
        return None

    print("Loaded:", filename)
    return loaded


def export_png(surface, filename):
    try:
        pg.image.save(surface, filename)
    except (OSError, pg.error):
        print("Could not export:", filename)
        return

    print("Exported:", filename)


# Initialize the window, data and tools.
pg.init()

ROWS = 8
COLS = 12
CELL_SIZE = 40
FPS = 60
SAVE_NPY = "pixel_art_rgb.npy"
EXPORT_PNG = "pixel_art_rgb.png"

BG_RGB = np.array([245, 245, 245], dtype=np.uint8)
GRID_COLOR = (185, 198, 206)

matrix = np.zeros((ROWS, COLS, 3), dtype=np.uint8)
matrix[:] = BG_RGB

matrix[:4, :6] = (230, 60, 60)
matrix[:4, 6:] = (60, 180, 90)
matrix[4:, :6] = (70, 110, 230)
matrix[4:, 6:] = (245, 205, 60)

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
    "pipette_cells": [],
    "erase": False,
    "clear": False,
    "save": False,
    "load": False,
    "export": False,
}

running = True

while running:
    # Read the event queue once.
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # Update the tools and modify the canvas.
    handle_controls(events, state, CELL_SIZE)
    apply_actions(matrix, state, BG_RGB)

    # Save or restore cell data before preparing the image.
    if state["save"]:
        save_matrix_npy(matrix, SAVE_NPY)

    if state["load"]:
        loaded = load_matrix_npy(SAVE_NPY, matrix.shape, matrix.dtype)
        if loaded is not None:
            matrix[:] = loaded

    # Show the current brush settings.
    r, g, b = state["brush_rgb"]
    channel = state["channel"]
    pg.display.set_caption(
        f"Module 11 | R={r} G={g} B={b} | channel={channel}"
    )

    # Keep the clean image separate from the interface.
    frame_surface = matrix_to_surface(matrix, CELL_SIZE)
    screen.blit(frame_surface, (0, 0))
    screen.blit(grid_surface, (0, 0))

    # Locate the cursor for this frame.
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

    # Export only the clean image, then display the whole frame.
    if state["export"]:
        export_png(frame_surface, EXPORT_PNG)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
