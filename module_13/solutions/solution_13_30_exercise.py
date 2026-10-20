# Matrix Thinking - Module 13: Maze as a Matrix
# A wall is 0; a passage is 1. Coordinates in maze are (row, col).
# The cursor uses (col, row), matching the screen's horizontal/vertical order.
#
# Controls:
#   Left click: try to open a passage. Right click: restore a wall.
#   G: start/pause growth. C: clear and stop. P: check and pause.
#   S: save maze.npy. L: load and pause. Esc: close the window.

import pygame as pg
import numpy as np

pg.init()

# Field dimensions are measured in cells; window dimensions are in pixels.
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


# Grid and input helpers

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
    # Commands last one frame; auto_grow and check_result persist.
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


# Local rules: one selected cell at a time

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


# Derived data: all allowed openings for the current maze

def build_frontier(maze):
    """Build allowed openings from four bounded neighbor contributions."""
    path_mask = maze == 1
    wall_mask = maze == 0

    # The first passage may be opened in any wall cell.
    if not np.any(path_mask):
        return wall_mask.astype(np.uint8)

    # Numeric counters store 0..4. Every contribution reads path_mask.
    neighbors = np.zeros_like(maze, dtype=np.uint8)
    neighbors[1:, :] += path_mask[:-1, :]   # Passage above the target cell
    neighbors[:-1, :] += path_mask[1:, :]   # Passage below the target cell
    neighbors[:, 1:] += path_mask[:, :-1]   # Passage left of the target cell
    neighbors[:, :-1] += path_mask[:, 1:]   # Passage right of the target cell

    frontier_mask = wall_mask & (neighbors == 1)
    return frontier_mask.astype(np.uint8)


# Automatic growth: choose and open exactly one allowed cell

def frontier_cells(frontier):
    """Find allowed openings with NumPy and return coordinate tuples."""
    coordinates = np.argwhere(frontier == 1)
    cells = []
    for row, col in coordinates:
        cells.append((int(row), int(col)))
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
    # The caller must rebuild frontier after this change.
    maze[row, col] = 1
    return True


# Persistence: save model data; recompute derived data after loading

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

    # A file must match both the array format and the maze value rules.
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


# Global checks: reachability and the tree criterion

def get_path_cells(maze):
    """Find passages with NumPy and return Python coordinate tuples."""
    coordinates = np.argwhere(maze == 1)
    cells = []
    for row, col in coordinates:
        cells.append((int(row), int(col)))
    return cells


def is_connected_paths(maze):
    """Check whether all passages are reachable from one starting cell."""
    path_cells = get_path_cells(maze)
    if len(path_cells) == 0:
        return False

    rows, cols = maze.shape
    start = path_cells[0]
    # stack holds pending work; visited includes every discovered cell.
    stack = [start]
    visited = {start}

    while stack:
        row, col = stack.pop()
        for neighbor in get_neighbors4(row, col, rows, cols):
            neighbor_row, neighbor_col = neighbor
            if maze[neighbor_row, neighbor_col] == 1 and neighbor not in visited:
                # Mark immediately so the same cell is never scheduled twice.
                visited.add(neighbor)
                stack.append(neighbor)

    return len(visited) == len(path_cells)


def count_edges_between_paths(maze):
    """Count vertical and horizontal passage pairs using aligned slices."""
    path_mask = maze == 1
    # Each adjacent pair is counted once; opposite edges never meet.
    vertical_pairs = path_mask[:-1, :] & path_mask[1:, :]
    horizontal_pairs = path_mask[:, :-1] & path_mask[:, 1:]

    vertical_edges = np.sum(vertical_pairs)
    horizontal_edges = np.sum(horizontal_pairs)
    return int(vertical_edges + horizontal_edges)


def is_perfect_maze(maze):
    """A nonempty connected passage graph is a tree when E = V - 1."""
    vertices = len(get_path_cells(maze))
    if vertices == 0:
        return False

    if not is_connected_paths(maze):
        return False

    # E = V - 1 is used only after proving connectivity.
    edges = count_edges_between_paths(maze)
    return edges == vertices - 1


# Manual changes report whether an earlier check result became stale.

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


# Rendering: compose display data without changing the maze

def reachable_cells(maze, start):
    """Find passages reachable from a valid (row, col) cell."""
    row, col = start
    if maze[row, col] != 1:
        return set()
    rows, cols = maze.shape
    stack = [start]
    visited = {start}
    while stack:
        row, col = stack.pop()
        for neighbor in get_neighbors4(row, col, rows, cols):
            nr, nc = neighbor
            if maze[nr, nc] == 1 and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return visited


def build_reachable_mask(maze, start):
    """Turn reachable coordinates into a display mask."""
    mask = np.zeros_like(maze, dtype=bool)
    for row, col in reachable_cells(maze, start):
        mask[row, col] = True
    return mask


def count_components(maze):
    """Count connected passage groups, including isolated passages."""
    visited = set()
    count = 0
    for start in get_path_cells(maze):
        if start not in visited:
            visited.update(reachable_cells(maze, start))
            count += 1
    return count


def build_frame_indices(maze, frontier):
    """Highlight allowed cells in an independent display array."""
    # Index 2 belongs only to the display array, never to maze.
    indices = maze.copy()
    indices[frontier == 1] = 2
    return indices


def indices_to_surface_fast(indices, palette, cell_size):
    """Map indices to RGB and enlarge each cell into a pixel block."""
    rgb = palette[indices]  # (rows, cols, 3)
    rgb = np.repeat(rgb, cell_size, axis=0)
    rgb = np.repeat(rgb, cell_size, axis=1)
    # repeat produced (height, width, 3); Pygame expects (width, height, 3).
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


# Initialize the window, model and reusable grid.
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
    "component_count": None,
    "auto_grow": False,
}

grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
pg.mouse.set_visible(False)

# Frame order: input -> manual/file changes -> frontier -> growth/check -> draw.
running = True
while running:
    events = pg.event.get()
    running = handle_quit(events)
    update_cursor(state, CELL_SIZE, ROWS, COLS)
    handle_controls(events, state, CELL_SIZE, ROWS, COLS)
    # Keep a check result only while it still describes the current maze.
    changed = apply_actions(maze, state)
    if changed:
        state["check_result"] = None
        state["component_count"] = None

    # Save/load refer to the model, without cursor or display colors.
    if state["save"]:
        save_maze(maze, MAZE_FILE)
    if state["load"]:
        loaded = load_maze(MAZE_FILE, maze.shape)
        if loaded is not None:
            maze = loaded
            state["auto_grow"] = False
            state["check_result"] = None
            state["component_count"] = None

    # Always choose from a frontier computed after the latest model change.
    frontier = build_frontier(maze)
    if state["auto_grow"]:
        grew = growth_step(maze, frontier)
        if grew:
            state["check_result"] = None
            state["component_count"] = None
            frontier = build_frontier(maze)
        else:
            state["auto_grow"] = False

    # P pauses growth, then checks the field that this frame will display.
    if state["check"]:
        state["check_result"] = is_perfect_maze(maze)
        state["component_count"] = count_components(maze)

    if state["auto_grow"]:
        title = "Maze | Auto: ON"
    else:
        title = "Maze | Auto: OFF"
    # None means no current result; False is a completed negative check.
    if state["check_result"] is None:
        title += " | Perfect: NOT CHECKED"
    elif state["check_result"]:
        title += " | Perfect: YES"
    else:
        title += " | Perfect: NO"
    if state["component_count"] is not None:
        title += f" | Components: {state['component_count']}"
    pg.display.set_caption(title)

    render(screen, maze, frontier, grid_surface, state, CELL_SIZE)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
