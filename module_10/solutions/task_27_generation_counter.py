import numpy as np
import pygame as pg


def life_calculation_roll(matrix):
    up = np.roll(matrix, 1, axis=0)
    down = np.roll(matrix, -1, axis=0)
    left = np.roll(matrix, 1, axis=1)
    right = np.roll(matrix, -1, axis=1)

    up_left = np.roll(up, 1, axis=1)
    up_right = np.roll(up, -1, axis=1)
    down_left = np.roll(down, 1, axis=1)
    down_right = np.roll(down, -1, axis=1)

    neighbors = (
        up + down + left + right
        + up_left + up_right + down_left + down_right
    )

    alive = matrix == 1
    survive = alive & ((neighbors == 2) | (neighbors == 3))
    born = (~alive) & (neighbors == 3)

    new_matrix = np.zeros_like(matrix)
    new_matrix[survive | born] = 1

    # Keep the outer border empty.
    new_matrix[0, :] = 0
    new_matrix[-1, :] = 0
    new_matrix[:, 0] = 0
    new_matrix[:, -1] = 0

    return new_matrix


def matrix_to_surface(matrix, palette, cell_size):
    image = palette[matrix]
    image = np.repeat(image, cell_size, axis=0)
    image = np.repeat(image, cell_size, axis=1)

    return pg.surfarray.make_surface(image.swapaxes(0, 1))


pg.init()

ROWS = 15
COLS = 21
CELL_SIZE = 32
FPS = 60
FRAMES_PER_GENERATION = 6

COLORS = np.array([
    [245, 247, 250],
    [22, 139, 145],
], dtype=np.uint8)

matrix = np.zeros((ROWS, COLS), dtype=np.uint8)

# Place a horizontal blinker at the centre.
y = ROWS // 2
x = COLS // 2
matrix[y, x - 1:x + 2] = 1

screen = pg.display.set_mode((
    COLS * CELL_SIZE,
    ROWS * CELL_SIZE,
))
pg.display.set_caption(
    "Game of Life | Space: run/pause | N: step | C: clear | S/L: save/load"
)

clock = pg.time.Clock()
running = True
simulation_running = False
generation_frames = 0
generation = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

            elif event.key == pg.K_SPACE:
                simulation_running = not simulation_running
                generation_frames = 0

            elif event.key == pg.K_n:
                if not simulation_running:
                    matrix = life_calculation_roll(matrix)
                    generation += 1
                    print(
                        f"Generation: {generation} | "
                        f"Living cells: {np.sum(matrix)}"
                    )

            elif event.key == pg.K_c:
                matrix.fill(0)
                generation = 0
                simulation_running = False
                generation_frames = 0

            elif event.key == pg.K_s:
                try:
                    np.save("life_world.npy", matrix)
                except OSError:
                    print("The world could not be saved.")

            elif event.key == pg.K_l:
                try:
                    loaded_matrix = np.load(
                        "life_world.npy",
                        allow_pickle=False,
                    )

                    if (
                        isinstance(loaded_matrix, np.ndarray)
                        and loaded_matrix.shape == matrix.shape
                        and np.all(
                            (loaded_matrix == 0) | (loaded_matrix == 1)
                        )
                    ):
                        matrix = loaded_matrix.astype(np.uint8)

                        # Keep the outer border empty.
                        matrix[0, :] = 0
                        matrix[-1, :] = 0
                        matrix[:, 0] = 0
                        matrix[:, -1] = 0

                        generation = 0
                        simulation_running = False
                        generation_frames = 0
                    else:
                        print("The file must contain a matching binary field.")

                except FileNotFoundError:
                    print("Save a world with S before loading it.")
                except (OSError, ValueError, EOFError):
                    print("The world file could not be read.")

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not simulation_running:
                x_px, y_px = event.pos
                x = x_px // CELL_SIZE
                y = y_px // CELL_SIZE

                if 1 <= y < ROWS - 1 and 1 <= x < COLS - 1:
                    matrix[y, x] = 1 - matrix[y, x]

    if simulation_running:
        generation_frames += 1

        if generation_frames >= FRAMES_PER_GENERATION:
            matrix = life_calculation_roll(matrix)
            generation += 1
            print(
                f"Generation: {generation} | "
                f"Living cells: {np.sum(matrix)}"
            )
            generation_frames = 0

    surface = matrix_to_surface(matrix, COLORS, CELL_SIZE)
    screen.blit(surface, (0, 0))

    if not simulation_running and pg.mouse.get_focused():
        x_px, y_px = pg.mouse.get_pos()
        x = x_px // CELL_SIZE
        y = y_px // CELL_SIZE

        if 1 <= y < ROWS - 1 and 1 <= x < COLS - 1:
            pg.draw.rect(
                screen,
                (210, 90, 45),
                (
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
                2,
            )

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
