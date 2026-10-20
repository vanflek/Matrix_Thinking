import pygame as pg
import numpy as np

pg.init()

ROWS = 32
COLS = 64
CELL_SIZE = 16

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 60
MAZE_FILE = "maze.npy"

PALETTE = np.array(
    [
        (20, 20, 20),       # 0: wall
        (240, 240, 240),    # 1: passage
        (35, 90, 60),       # 2: allowed opening (display only)
    ],
    dtype=np.uint8
)
GRID_COLOR = (185, 198, 206)
CURSOR_OK = (0, 200, 0)
CURSOR_NO = (220, 60, 60)


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
    state["save"] = False
    state["load"] = False
    state["check"] = False

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
                state["auto_grow"] = False
            elif event.key == pg.K_g:
                state["auto_grow"] = not state["auto_grow"]
            elif event.key == pg.K_s:
                state["save"] = True
            elif event.key == pg.K_l:
                state["load"] = True
            elif event.key == pg.K_p:
                state["check"] = True
                state["auto_grow"] = False


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


def build_frontier(maze):
    """Mark every cell that can be opened in the current maze."""
    rows, cols = maze.shape
    frontier = np.zeros_like(maze)

    for row in range(rows):
        for col in range(cols):
            if can_open_by_local_rule(maze, row, col):
                frontier[row, col] = 1

    return frontier


def frontier_cells(frontier):
    """Collect allowed cell coordinates in row-major order."""
    rows, cols = frontier.shape
    cells = []

    for row in range(rows):
        for col in range(cols):
            if frontier[row, col] == 1:
                cells.append((row, col))

    return cells


def choose_next_frontier_cell(frontier):
    """Return one random allowed cell, or None if no cells are allowed."""
    cells = frontier_cells(frontier)
    if len(cells) == 0:
        return None

    index = np.random.randint(len(cells))
    return cells[index]


def growth_step(maze, frontier):
    """Open one cell using a frontier computed from the current maze."""
    cell = choose_next_frontier_cell(frontier)
    if cell is None:
        return False

    row, col = cell
    maze[row, col] = 1
    return True


def save_maze(maze, filename):
    """Save only the maze matrix, without display or control state."""
    try:
        np.save(filename, maze)
    except OSError:
        print("Could not save:", filename)
        return

    print("Saved:", filename)


def load_maze(filename, expected_shape):
    """Return a matching binary uint8 matrix, or None if loading fails."""
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

    if loaded.dtype != np.uint8:
        print("Expected a uint8 matrix.")
        return None

    if not np.all((loaded == 0) | (loaded == 1)):
        print("Expected only 0 and 1.")
        return None

    print("Loaded:", filename)
    return loaded


def get_path_cells(maze):
    """Collect all passage coordinates without changing the maze."""
    rows, cols = maze.shape
    cells = []

    for row in range(rows):
        for col in range(cols):
            if maze[row, col] == 1:
                cells.append((row, col))

    return cells


def is_connected_paths(maze):
    """Check whether all passages are reachable from one starting cell."""
    path_cells = get_path_cells(maze)
    if len(path_cells) == 0:
        return False

    rows, cols = maze.shape
    start = path_cells[0]
    stack = [start]
    visited = {start}

    while stack:
        row, col = stack.pop()
        for neighbor in get_neighbors4(row, col, rows, cols):
            neighbor_row, neighbor_col = neighbor
            if maze[neighbor_row, neighbor_col] == 1 and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return len(visited) == len(path_cells)


def count_edges_between_paths(maze):
    """Count each connection once by looking only down and right."""
    rows, cols = maze.shape
    edges = 0

    for row in range(rows):
        for col in range(cols):
            if maze[row, col] != 1:
                continue

            if row + 1 < rows and maze[row + 1, col] == 1:
                edges += 1
            if col + 1 < cols and maze[row, col + 1] == 1:
                edges += 1

    return edges


def is_perfect_maze(maze):
    """A nonempty connected passage graph is a tree when E = V - 1."""
    vertices = len(get_path_cells(maze))
    if vertices == 0:
        return False

    if not is_connected_paths(maze):
        return False

    edges = count_edges_between_paths(maze)
    return edges == vertices - 1


def apply_actions(maze, state):
    """Apply manual commands and return whether maze values changed."""
    col, row = state["cell"]
    changed = False

    if state["clear"]:
        changed = np.any(maze == 1)
        maze[:] = 0
    elif state["paint_wall"]:
        changed = maze[row, col] == 1
        maze[row, col] = 0
    elif state["paint_path"]:
        if can_open_by_local_rule(maze, row, col):
            maze[row, col] = 1
            changed = True

    return changed


def build_frame_indices(maze, frontier):
    """Highlight allowed cells in an independent display array."""
    indices = maze.copy()
    indices[frontier == 1] = 2
    return indices


def indices_to_surface_fast(indices, palette, cell_size):
    """Map indices to RGB and enlarge each cell into a pixel block."""
    rgb = palette[indices]
    rgb = np.repeat(rgb, cell_size, axis=0)
    rgb = np.repeat(rgb, cell_size, axis=1)
    return pg.surfarray.make_surface(np.swapaxes(rgb, 0, 1))


def render(screen, maze, frontier, grid_surface, state, cell_size):
    """Show passages, allowed openings, the grid and the cursor."""
    indices = build_frame_indices(maze, frontier)
    frame = indices_to_surface_fast(indices, PALETTE, cell_size)
    screen.blit(frame, (0, 0))
    screen.blit(grid_surface, (0, 0))

    col, row = state["cell"]
    if frontier[row, col] == 1:
        outline_color = CURSOR_OK
    else:
        outline_color = CURSOR_NO

    pg.draw.rect(
        screen,
        outline_color,
        (col * cell_size, row * cell_size, cell_size, cell_size),
        3
    )


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Maze | Auto: OFF | Perfect: NOT CHECKED")
clock = pg.time.Clock()

# The maze stores walls and passages; the cursor has its own state.
maze = np.zeros((ROWS, COLS), dtype=np.uint8)
state = {
    "cell": (0, 0),
    "paint_path": False,
    "paint_wall": False,
    "clear": False,
    "save": False,
    "load": False,
    "check": False,
    "check_result": None,
    "auto_grow": False,
}

grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
pg.mouse.set_visible(False)

running = True
while running:
    events = pg.event.get()
    running = handle_quit(events)
    update_cursor(state, CELL_SIZE, ROWS, COLS)
    handle_controls(events, state, CELL_SIZE, ROWS, COLS)
    changed = apply_actions(maze, state)
    if changed:
        state["check_result"] = None

    if state["save"]:
        save_maze(maze, MAZE_FILE)
    if state["load"]:
        loaded = load_maze(MAZE_FILE, maze.shape)
        if loaded is not None:
            maze = loaded
            state["auto_grow"] = False
            state["check_result"] = None

    frontier = build_frontier(maze)
    if state["auto_grow"]:
        grew = growth_step(maze, frontier)
        if grew:
            state["check_result"] = None
            frontier = build_frontier(maze)
        else:
            state["auto_grow"] = False

    if state["check"]:
        state["check_result"] = is_perfect_maze(maze)

    if state["auto_grow"]:
        title = "Maze | Auto: ON"
    else:
        title = "Maze | Auto: OFF"
    if state["check_result"] is None:
        title += " | Perfect: NOT CHECKED"
    elif state["check_result"]:
        title += " | Perfect: YES"
    else:
        title += " | Perfect: NO"
    pg.display.set_caption(title)

    render(screen, maze, frontier, grid_surface, state, CELL_SIZE)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
