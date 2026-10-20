import pygame as pg
import numpy as np

pg.init()

ROWS = 32
COLS = 64
CELL_SIZE = 16

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 60

PALETTE = np.array(
    [
        (20, 20, 20),       # 0: wall
        (240, 240, 240),    # 1: passage
    ],
    dtype=np.uint8
)
GRID_COLOR = (185, 198, 206)
CURSOR_COLOR = (0, 200, 0)


def build_grid_surface(rows, cols, cell_size, grid_color):
    """Draw the grid once and reuse it in every frame."""
    width = cols * cell_size
    height = rows * cell_size
    grid = pg.Surface((width, height), pg.SRCALPHA)
    grid.fill((0, 0, 0, 0))

    for row in range(1, rows):
        y = row * cell_size
        pg.draw.line(grid, grid_color, (0, y), (width - 1, y))

    for col in range(1, cols):
        x = col * cell_size
        pg.draw.line(grid, grid_color, (x, 0), (x, height - 1))

    # Keep all four borders inside the surface.
    pg.draw.rect(grid, grid_color, (0, 0, width, height), 1)
    return grid


def clamp_cell(col, row, rows, cols):
    """Keep the selected cell inside the matrix."""
    col = max(0, min(col, cols - 1))
    row = max(0, min(row, rows - 1))
    return col, row


def update_cursor(state, cell_size, rows, cols):
    """Convert mouse pixels to a column and a row."""
    x, y = pg.mouse.get_pos()
    col = x // cell_size
    row = y // cell_size
    state["cell"] = clamp_cell(col, row, rows, cols)


def handle_quit(events):
    """Return False when the user closes the window or presses Esc."""
    for event in events:
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
    return True


def handle_controls(events, state, cell_size, rows, cols):
    """Translate input events into commands for the current frame."""
    state["paint_path"] = False
    state["paint_wall"] = False
    state["clear"] = False

    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                # Use the click position, even if the mouse has moved since.
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size
                state["cell"] = clamp_cell(col, row, rows, cols)
                state["paint_path"] = event.button == 1
                state["paint_wall"] = event.button == 3

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                state["clear"] = True


def get_neighbors4(row, col, rows, cols):
    """Return valid neighbors in the order: up, down, left, right."""
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))

    return neighbors


def count_path_neighbors(maze, row, col):
    """Count passages among valid neighbors of the selected cell."""
    rows, cols = maze.shape
    count = 0

    for neighbor_row, neighbor_col in get_neighbors4(row, col, rows, cols):
        if maze[neighbor_row, neighbor_col] == 1:
            count += 1

    return count


def has_any_path_cells(maze):
    """Return True if the maze contains at least one passage."""
    return np.any(maze == 1)


def can_open_by_local_rule(maze, row, col):
    """Check a valid cell without changing the maze."""
    if maze[row, col] != 0:
        return False

    if not has_any_path_cells(maze):
        return True

    return count_path_neighbors(maze, row, col) == 1


def apply_actions(maze, state):
    """Apply commands; open a passage only when the local rule allows it."""
    col, row = state["cell"]

    if state["clear"]:
        maze[:] = 0
    elif state["paint_wall"]:
        maze[row, col] = 0
    elif state["paint_path"]:
        if can_open_by_local_rule(maze, row, col):
            maze[row, col] = 1


def indices_to_surface_fast(indices, palette, cell_size):
    """Map indices to RGB and enlarge each cell into a pixel block."""
    rgb = palette[indices]
    rgb = np.repeat(rgb, cell_size, axis=0)
    rgb = np.repeat(rgb, cell_size, axis=1)
    return pg.surfarray.make_surface(np.swapaxes(rgb, 0, 1))


def render(screen, maze, grid_surface, state, cell_size):
    """Draw the maze, the grid and the cursor without changing maze."""
    frame = indices_to_surface_fast(maze, PALETTE, cell_size)
    screen.blit(frame, (0, 0))
    screen.blit(grid_surface, (0, 0))

    col, row = state["cell"]
    pg.draw.rect(
        screen,
        CURSOR_COLOR,
        (col * cell_size, row * cell_size, cell_size, cell_size),
        3
    )


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Maze: local growth rule")
clock = pg.time.Clock()

# The maze stores walls and passages; the cursor has its own state.
maze = np.zeros((ROWS, COLS), dtype=np.uint8)
state = {
    "cell": (0, 0),
    "paint_path": False,
    "paint_wall": False,
    "clear": False,
}

grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
pg.mouse.set_visible(False)

running = True
while running:
    events = pg.event.get()
    running = handle_quit(events)
    update_cursor(state, CELL_SIZE, ROWS, COLS)
    handle_controls(events, state, CELL_SIZE, ROWS, COLS)
    apply_actions(maze, state)

    render(screen, maze, grid_surface, state, CELL_SIZE)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
