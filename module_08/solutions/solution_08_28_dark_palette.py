import pygame as pg
import numpy as np

ROWS = 16
COLS = 16
CELL_SIZE = 40
FPS = 60
STEP_FRAMES = 6

COLORS = np.array([
    [25, 30, 40],
    [0, 0, 0],
    [255, 255, 255],
    [255, 190, 60],
    [0, 255, 0],
    [70, 210, 190],
], dtype=np.uint8)

TARGET_COLOR_INDEX = 3
PLAYER_COLOR_INDEX = 5
GRID_COLOR = (70, 80, 95)


# Read the same event list that is later used for movement.
def handle_quit(events):
    for event in events:
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False

    return True


# Change the existing direction vector; do not move the player yet.
def handle_input(events, state):
    movement = state["vel"]

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                movement[:] = (-1, 0)
            elif event.key == pg.K_DOWN:
                movement[:] = (1, 0)
            elif event.key == pg.K_LEFT:
                movement[:] = (0, -1)
            elif event.key == pg.K_RIGHT:
                movement[:] = (0, 1)


# Wrap row and column separately using the field shape.
def move_player(state, shape):
    position = state["pos"]
    movement = state["vel"]

    state["pos"] = (position + movement) % np.array(shape)


# Remove a whole coordinate row, then stop this function call.
def collect_target(state):
    position = state["pos"]

    for index, target in enumerate(state["targets"]):
        if position[0] == target[0] and position[1] == target[1]:
            state["targets"] = np.delete(
                state["targets"], index, axis=0
            )
            return


# Rebuild the display data from the current game state.
def rebuild_matrix(matrix, state):
    matrix.fill(0)

    for row, col in state["targets"]:
        matrix[row, col] = TARGET_COLOR_INDEX

    row, col = state["pos"]
    matrix[row, col] = PLAYER_COLOR_INDEX


# Select RGB vectors, enlarge spatial axes, then adapt the axis order.
def matrix_to_surface(matrix, palette, cell_size):
    rgb_small = palette[matrix]

    rgb_rows = np.repeat(rgb_small, cell_size, axis=0)
    rgb_big = np.repeat(rgb_rows, cell_size, axis=1)

    rgb_for_pygame = np.swapaxes(rgb_big, 0, 1)
    image = pg.surfarray.make_surface(rgb_for_pygame)

    return image


# Transparent pixels let the field remain visible under the grid.
def build_grid_surface(rows, cols, cell_size, grid_color):
    width = cols * cell_size
    height = rows * cell_size

    grid_surface = pg.Surface((width, height), pg.SRCALPHA)
    grid_surface.fill((0, 0, 0, 0))

    for col in range(1, cols):
        x = col * cell_size
        pg.draw.line(
            grid_surface, grid_color,
            (x, 0), (x, height - 1), 1
        )

    for row in range(1, rows):
        y = row * cell_size
        pg.draw.line(
            grid_surface, grid_color,
            (0, y), (width - 1, y), 1
        )

    pg.draw.rect(
        grid_surface, grid_color,
        (0, 0, width, height), 1
    )

    return grid_surface


pg.init()

screen = pg.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pg.display.set_caption("Collector")
clock = pg.time.Clock()

matrix = np.zeros((ROWS, COLS), dtype=np.uint8)

state = {
    "pos": np.array([8, 8], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([
        [2, 3],
        [5, 10],
        [12, 6],
    ], dtype=np.int16),
}

# Prepare the unchanged grid once.
grid_surface = build_grid_surface(
    ROWS, COLS, CELL_SIZE, GRID_COLOR
)

step_counter = 0
running = True

# Events and rendering continue even when no movement step is due.
while running:
    clock.tick(FPS)
    events = pg.event.get()
    running = handle_quit(events)

    if running:
        if len(state["targets"]) > 0:
            handle_input(events, state)
            step_counter += 1

            if step_counter >= STEP_FRAMES:
                step_counter = 0

                move_player(state, matrix.shape)
                collect_target(state)

                if len(state["targets"]) == 0:
                    pg.display.set_caption("Collector - You win!")
                    print("All targets collected!")

        rebuild_matrix(matrix, state)
        field_surface = matrix_to_surface(
            matrix, COLORS, CELL_SIZE
        )

        screen.blit(field_surface, (0, 0))
        screen.blit(grid_surface, (0, 0))
        pg.display.flip()

pg.quit()
