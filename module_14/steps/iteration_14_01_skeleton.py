import pygame as pg
import numpy as np

pg.init()

ROWS = 16
COLS = 32
CELL_SIZE = 32

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

PALETTE = np.array([
    (20, 20, 20),
    (0, 200, 255),
    (255, 120, 0),
    (255, 255, 0)
], dtype=np.uint8)

GRID_COLOR = (185, 198, 206)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Module 14 - Bug Buster: skeleton")
clock = pg.time.Clock()

# Store object positions in separate binary layers.
world = np.zeros((ROWS, COLS, LAYERS), dtype=np.uint8)
world[ROWS // 2, COLS // 2, LAYER_PLAYER] = 1
world[ROWS // 3, COLS // 3, LAYER_BUG] = 1

assert world[:, :, LAYER_PLAYER].sum() == 1
assert world[:, :, LAYER_BUG].sum() == 1


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


def render(screen, world_3d, grid_surface, cell_size):
    """Display the world, then overlay the reusable grid."""
    indices = compose_screen_indices(world_3d)
    frame = indices_to_surface_fast(indices, PALETTE, cell_size)
    screen.blit(frame, (0, 0))
    screen.blit(grid_surface, (0, 0))


grid_surface = build_grid_surface(
    ROWS, COLS, CELL_SIZE, GRID_COLOR
)

running = True
while running:
    events = pg.event.get()
    running = handle_quit(events)

    render(screen, world, grid_surface, CELL_SIZE)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
