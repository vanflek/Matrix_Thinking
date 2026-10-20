import numpy as np
import pygame as pg


ROWS = 20
COLS = 10
CELL_SIZE = 30
FPS = 60

FIXED_LAYER = 0
ACTIVE_LAYER = 1
GRID_COLOR = (200, 210, 220, 110)

COLORS = np.array([
    [255, 255, 255],  # 0 - empty
    [0, 240, 240],    # 1 - I
    [240, 240, 0],    # 2 - O
    [170, 70, 220],   # 3 - T
    [255, 150, 0],    # 4 - L
    [0, 90, 230],     # 5 - J
    [0, 200, 80],     # 6 - S
    [230, 50, 50],    # 7 - Z
], dtype=np.uint8)


TETROMINOES = {
    "I": np.array([
        [1, 1, 1, 1],
    ], dtype=np.uint8),

    "O": np.array([
        [2, 2],
        [2, 2],
    ], dtype=np.uint8),

    "T": np.array([
        [0, 3, 0],
        [3, 3, 3],
    ], dtype=np.uint8),

    "L": np.array([
        [4, 0],
        [4, 0],
        [4, 4],
    ], dtype=np.uint8),

    "J": np.array([
        [0, 5],
        [0, 5],
        [5, 5],
    ], dtype=np.uint8),

    "S": np.array([
        [0, 6, 6],
        [6, 6, 0],
    ], dtype=np.uint8),

    "Z": np.array([
        [7, 7, 0],
        [0, 7, 7],
    ], dtype=np.uint8),
}


class Tetromino:
    def __init__(self, matrix, x=0, y=0, rotation=0):
        self.matrix = matrix.copy()
        self.x = x
        self.y = y
        self.rotation = rotation

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_matrix(self):
        return np.rot90(self.matrix, self.rotation)


class GameModel:
    def __init__(self, rows=ROWS, cols=COLS):
        self.glass = np.zeros((2, rows, cols), dtype=np.uint8)
        self.new_tetromino()

    def new_tetromino(self):
        name = np.random.choice(list(TETROMINOES))
        matrix = TETROMINOES[name]
        cols = self.glass.shape[2]
        x = (cols - matrix.shape[1]) // 2
        self.current_tetromino = Tetromino(matrix, x=x, y=0)


class InputController:
    def get_actions(self):
        actions = {
            "move_left": False,
            "move_right": False,
            "move_down": False,
            "rotate": False,
            "lock": False,
            "quit": False,
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True
                elif event.key == pg.K_LEFT:
                    actions["move_left"] = True
                elif event.key == pg.K_RIGHT:
                    actions["move_right"] = True
                elif event.key == pg.K_DOWN:
                    actions["move_down"] = True
                elif event.key == pg.K_UP:
                    actions["rotate"] = True
                elif event.key == pg.K_SPACE:
                    # Temporary manual locking for this learning stage.
                    actions["lock"] = True

        return actions


class GameLogic:
    def update_active_layer(self, model):
        piece = model.current_tetromino
        matrix = piece.get_matrix()
        height, width = matrix.shape

        active_layer = model.glass[ACTIVE_LAYER]
        active_layer.fill(0)
        active_layer[
            piece.y:piece.y + height,
            piece.x:piece.x + width,
        ] = matrix

    def try_transform(self, model, dx=0, dy=0, rotate=False):
        piece = model.current_tetromino
        old_x = piece.x
        old_y = piece.y
        old_rotation = piece.rotation

        piece.move(dx, dy)
        if rotate:
            piece.rotate()

        height, width = piece.get_matrix().shape
        rows, cols = model.glass.shape[1:]
        inside = (
            piece.x >= 0
            and piece.y >= 0
            and piece.x + width <= cols
            and piece.y + height <= rows
        )

        if not inside:
            piece.x = old_x
            piece.y = old_y
            piece.rotation = old_rotation
            return False

        self.update_active_layer(model)
        return True

    def lock_tetromino(self, model):
        fixed_layer = model.glass[FIXED_LAYER]
        active_layer = model.glass[ACTIVE_LAYER]

        mask = active_layer != 0
        fixed_layer[mask] = active_layer[mask]

        model.new_tetromino()
        self.update_active_layer(model)

    def step(self, model, actions):
        self.update_active_layer(model)

        if actions["move_left"]:
            self.try_transform(model, dx=-1)
        if actions["move_right"]:
            self.try_transform(model, dx=1)
        if actions["move_down"]:
            self.try_transform(model, dy=1)
        if actions["rotate"]:
            self.try_transform(model, rotate=True)
        if actions["lock"]:
            self.lock_tetromino(model)


class GameView:
    def __init__(self, screen, cell_size=CELL_SIZE):
        self.screen = screen
        self.cell_size = cell_size
        self.grid = self.make_grid()

    def make_grid(self):
        width, height = self.screen.get_size()
        grid = pg.Surface((width, height), pg.SRCALPHA)
        grid.fill((0, 0, 0, 0))

        for y in range(0, height, self.cell_size):
            pg.draw.line(grid, GRID_COLOR, (0, y), (width - 1, y))
        for x in range(0, width, self.cell_size):
            pg.draw.line(grid, GRID_COLOR, (x, 0), (x, height - 1))

        pg.draw.rect(grid, GRID_COLOR, (0, 0, width, height), 1)
        return grid

    def draw(self, glass):
        fixed = glass[FIXED_LAYER]
        active = glass[ACTIVE_LAYER]
        cells = np.where(active != 0, active, fixed)

        pixels = COLORS[cells]
        pixels = np.repeat(pixels, self.cell_size, axis=0)
        pixels = np.repeat(pixels, self.cell_size, axis=1)

        pg.surfarray.blit_array(self.screen, np.swapaxes(pixels, 0, 1))
        self.screen.blit(self.grid, (0, 0))


class GameApp:
    def __init__(self):
        pg.init()
        self.model = GameModel()
        self.controller = InputController()
        self.logic = GameLogic()

        rows, cols = self.model.glass.shape[1:]
        self.screen = pg.display.set_mode(
            (cols * CELL_SIZE, rows * CELL_SIZE)
        )
        pg.display.set_caption("Matrix Tetris - Skeleton")

        self.view = GameView(self.screen)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            actions = self.controller.get_actions()

            if actions["quit"]:
                self.running = False
            else:
                self.logic.step(self.model, actions)
                self.view.draw(self.model.glass)
                pg.display.flip()

        pg.quit()


app = GameApp()
app.run()
