import pygame as pg
import numpy as np

ROWS = 16
COLS = 16
CELL_SIZE = 40
FPS = 60
STEP_FRAMES = 6

COLORS = np.array([
    [245, 245, 245],
    [0, 0, 0],
    [255, 255, 255],
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
], dtype=np.uint8)
GRID_COLOR = (80, 80, 80)


# Return whether the window should remain open.
def handle_quit(events):
    for event in events:
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False

    return True


# Accept at most one perpendicular turn before the next movement step.
def change_direction(state, new_direction):
    if not state["can_turn"]:
        return

    if np.array_equal(new_direction, state["vel"]):
        return

    if np.array_equal(new_direction, -state["vel"]):
        return

    state["vel"] = new_direction
    state["can_turn"] = False


# Translate arrow events into proposed direction vectors.
def handle_input(events, state):
    for event in events:
        if event.type == pg.KEYDOWN:
            new_direction = None

            if event.key == pg.K_UP:
                new_direction = np.array([-1, 0], dtype=np.int16)
            elif event.key == pg.K_DOWN:
                new_direction = np.array([1, 0], dtype=np.int16)
            elif event.key == pg.K_LEFT:
                new_direction = np.array([0, -1], dtype=np.int16)
            elif event.key == pg.K_RIGHT:
                new_direction = np.array([0, 1], dtype=np.int16)

            if new_direction is not None:
                change_direction(state, new_direction)


# Ignore the departing tail unless this step grows the snake.
def hits_body(new_head, snake, eating):
    if eating:
        body = snake
    else:
        body = snake[1:]

    matches = body == new_head
    same_cell = matches.all(axis=1)

    return same_cell.any()


# Check the proposed move before committing a new coordinate array.
def do_snake_step(state, field_size):
    snake = state["snake"]

    new_head = (snake[-1] + state["vel"]) % field_size
    eating = np.array_equal(new_head, state["apple"])

    if hits_body(new_head, snake, eating):
        state["alive"] = False
        return

    snake = np.vstack((snake, new_head))

    if not eating:
        snake = snake[1:]

    state["snake"] = snake

    if eating:
        state["apple"] = None

    # Restore permission only after a completed movement step.
    state["can_turn"] = True


# Rebuild occupancy from the current snake coordinates.
def fill_field(matrix, snake):
    matrix[:] = 0
    matrix[snake[:, 0], snake[:, 1]] = 5


# Choose only among free cells; None means the field is full.
def spawn_apple(matrix):
    free_cells = np.argwhere(matrix == 0)

    if len(free_cells) == 0:
        return None

    index = np.random.randint(len(free_cells))
    return free_cells[index]


# Look up RGB colors, enlarge cells, and adapt axes to Pygame.
def matrix_to_surface(matrix, palette, cell_size):
    rgb_small = palette[matrix]

    rgb_rows = np.repeat(rgb_small, cell_size, axis=0)
    rgb_big = np.repeat(rgb_rows, cell_size, axis=1)

    rgb_for_pygame = np.swapaxes(rgb_big, 0, 1)
    image = pg.surfarray.make_surface(rgb_for_pygame)

    return image


# Build the unchanged transparent grid once.
def build_grid_surface(rows, cols, cell_size, grid_color):
    width = cols * cell_size
    height = rows * cell_size

    grid_surface = pg.Surface((width, height), pg.SRCALPHA)
    grid_surface.fill((0, 0, 0, 0))

    for col in range(1, cols):
        x = col * cell_size
        pg.draw.line(
            grid_surface, grid_color,
            (x, 0), (x, height - 1)
        )

    for row in range(1, rows):
        y = row * cell_size
        pg.draw.line(
            grid_surface, grid_color,
            (0, y), (width - 1, y)
        )

    pg.draw.rect(
        grid_surface, grid_color,
        (0, 0, width, height), 1
    )

    return grid_surface


pg.init()
screen = pg.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pg.display.set_caption("Snake")
clock = pg.time.Clock()

matrix = np.zeros((ROWS, COLS), dtype=np.uint8)
field_size = np.array(matrix.shape)
# Place the middle segment at the center of the field.
center_row = ROWS // 2
center_col = COLS // 2
state = {
    "snake": np.array([
        [center_row, center_col - 1],
        [center_row, center_col],
        [center_row, center_col + 1],
    ], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "apple": None,
    "alive": True,
    "won": False,
    "can_turn": True,
}

initial_length = len(state["snake"])
fill_field(matrix, state["snake"])
state["apple"] = spawn_apple(matrix)
state["won"] = state["apple"] is None
if state["apple"] is not None:
    row, col = state["apple"]
    matrix[row, col] = 3

grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
step_counter = 0
running = True

while running:
    clock.tick(FPS)
    events = pg.event.get()
    running = handle_quit(events)

    if running:
        if state["alive"] and not state["won"]:
            handle_input(events, state)
            step_counter += 1

            if step_counter >= STEP_FRAMES:
                step_counter = 0
                do_snake_step(state, field_size)

                if state["alive"]:
                    # Update occupancy before searching for a new apple.
                    fill_field(matrix, state["snake"])

                    if state["apple"] is None:
                        state["apple"] = spawn_apple(matrix)
                        state["won"] = state["apple"] is None

                    if state["apple"] is not None:
                        row, col = state["apple"]
                        matrix[row, col] = 3

        apples = len(state["snake"]) - initial_length

        if not state["alive"]:
            title = f"Snake - Game over - Apples: {apples}"
        elif state["won"]:
            title = f"Snake - You win! - Apples: {apples}"
        else:
            title = f"Snake - Apples: {apples}"

        pg.display.set_caption(title)

        # Keep displaying the last state after victory or defeat.
        field_surface = matrix_to_surface(matrix, COLORS, CELL_SIZE)
        screen.blit(field_surface, (0, 0))
        screen.blit(grid_surface, (0, 0))
        pg.display.flip()

pg.quit()
