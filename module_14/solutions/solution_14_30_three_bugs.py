# Standalone solution for Exercise 14.30.
import pygame as pg
import numpy as np
pg.init()
ROWS = 16
COLS = 32
CELL_SIZE = 32
LIGHT_RADIUS = 5
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 60
LAYER_PLAYER = 0
LAYER_BUG = 1
LAYERS = 2
IDX_BG = 0
IDX_PLAYER = 1
IDX_BUG = 2
IDX_OVERLAP = 3
PALETTE = np.array([(20, 20, 20), (0, 200, 255), (255, 120, 0), (255, 255, 0)], dtype=np.uint8)
GRID_COLOR = (185, 198, 206)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Module 14 - Bug Buster: flashlight')
clock = pg.time.Clock()
world = np.zeros((ROWS, COLS, LAYERS), dtype=np.uint8)
world[ROWS // 2, COLS // 2, LAYER_PLAYER] = 1
world[2, 3, LAYER_BUG] = 1
world[5, 10, LAYER_BUG] = 1
world[12, 25, LAYER_BUG] = 1
assert world[:, :, LAYER_PLAYER].sum() == 1
assert world[:, :, LAYER_BUG].sum() == 3

def build_grid_surface(rows, cols, cell_size, color):
    """Build a transparent grid once, including the outer edges."""
    width = cols * cell_size
    height = rows * cell_size
    surface = pg.Surface((width, height), pg.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    for row in range(rows + 1):
        y = min(row * cell_size, height - 1)
        pg.draw.line(surface, color, (0, y), (width - 1, y))
    for col in range(cols + 1):
        x = min(col * cell_size, width - 1)
        pg.draw.line(surface, color, (x, 0), (x, height - 1))
    return surface

def handle_quit(events):
    """Return False on a close request or an Escape keypress."""
    for event in events:
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
    return True

def build_shift_operators(cols, rows):
    """Build cyclic shifts for both field axes."""
    Cx_right = np.zeros((cols, cols), dtype=np.uint8)
    j = np.arange(cols)
    Cx_right[j, (j + 1) % cols] = 1
    Cy_down = np.zeros((rows, rows), dtype=np.uint8)
    i = np.arange(rows)
    Cy_down[(i + 1) % rows, i] = 1
    Cx_left = Cx_right.T
    Cy_up = Cy_down.T
    return (Cx_left, Cx_right, Cy_up, Cy_down)

def handle_controls(events):
    """Return the first supported command without modifying the world."""
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                return 'LEFT'
            elif event.key == pg.K_RIGHT:
                return 'RIGHT'
            elif event.key == pg.K_UP:
                return 'UP'
            elif event.key == pg.K_DOWN:
                return 'DOWN'
            elif event.key == pg.K_SPACE:
                return 'SPACE'
    return None

def respawn_bug(world_3d):
    """Replace only the captured bug, preserving all other bugs."""
    player = world_3d[:, :, LAYER_PLAYER]
    bug = world_3d[:, :, LAYER_BUG]
    overlap = player * bug
    if not overlap.any():
        return
    free_cells = np.argwhere((player == 0) & (bug == 0))
    if len(free_cells) == 0:
        return
    index = np.random.randint(len(free_cells))
    row, col = free_cells[index]
    bug[overlap == 1] = 0
    bug[row, col] = 1
    assert bug.sum() == 3

def apply_action(world_3d, action, Cx_left, Cx_right, Cy_up, Cy_down):
    """Move the player or attempt a capture on Space."""
    if action is None:
        return
    player = world_3d[:, :, LAYER_PLAYER]
    if action == 'LEFT':
        player = player @ Cx_left
    elif action == 'RIGHT':
        player = player @ Cx_right
    elif action == 'UP':
        player = Cy_up @ player
    elif action == 'DOWN':
        player = Cy_down @ player
    elif action == 'SPACE':
        bug = world_3d[:, :, LAYER_BUG]
        overlap = player * bug
        if overlap.any():
            respawn_bug(world_3d)
    world_3d[:, :, LAYER_PLAYER] = player

def compose_screen_indices(world_3d):
    """Build display indices without changing the world."""
    player = world_3d[:, :, LAYER_PLAYER]
    bug = world_3d[:, :, LAYER_BUG]
    indices = np.zeros(world_3d.shape[:2], dtype=np.uint8)
    indices[bug == 1] = IDX_BUG
    indices[player == 1] = IDX_PLAYER
    overlap = player * bug
    indices[overlap == 1] = IDX_OVERLAP
    return indices

def indices_to_surface_fast(indices, palette, cell_size):
    """Look up RGB colors, enlarge cells, and prepare Pygame axes."""
    rgb_small = palette[indices]
    rgb_big = np.repeat(rgb_small, cell_size, axis=0)
    rgb_big = np.repeat(rgb_big, cell_size, axis=1)
    rgb_for_pg = np.swapaxes(rgb_big, 0, 1)
    return pg.surfarray.make_surface(rgb_for_pg)

def build_light_mask(player_layer, radius):
    """Return a circular visibility mask without changing the player layer."""
    rows, cols = player_layer.shape
    pr, pc = np.argwhere(player_layer == 1)[0]
    Y, X = np.ogrid[:rows, :cols]
    dist2 = (Y - pr) ** 2 + (X - pc) ** 2
    light = (dist2 <= radius ** 2).astype(np.uint8)
    return light

def render(screen, world_3d, grid_surface, cell_size, light_radius):
    """Apply visibility to display indices, then overlay the grid."""
    indices = compose_screen_indices(world_3d)
    player = world_3d[:, :, LAYER_PLAYER]
    light = build_light_mask(player, light_radius)
    lit_indices = indices * light
    frame = indices_to_surface_fast(lit_indices, PALETTE, cell_size)
    screen.blit(frame, (0, 0))
    screen.blit(grid_surface, (0, 0))
Cx_left, Cx_right, Cy_up, Cy_down = build_shift_operators(COLS, ROWS)
grid_surface = build_grid_surface(ROWS, COLS, CELL_SIZE, GRID_COLOR)
running = True
while running:
    events = pg.event.get()
    running = handle_quit(events)
    action = handle_controls(events)
    apply_action(world, action, Cx_left, Cx_right, Cy_up, Cy_down)
    render(screen, world, grid_surface, CELL_SIZE, LIGHT_RADIUS)
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
