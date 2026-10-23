import numpy as np
import pygame as pg


ROWS = 32
COLS = 48
CELL_SIZE = 20
FPS = 60

TERRITORY_LAYER = 0
TRAIL_LAYER = 1
PLAYER_LAYER = 2
GRID_COLOR = (200, 210, 220, 80)

COLORS = np.array([
    [24, 30, 42],     # 0 - free space
    [65, 115, 160],   # 1 - territory
    [245, 185, 60],   # 2 - unfinished trail
    [245, 245, 245],  # 3 - player
], dtype=np.uint8)


class GameModel:
    def __init__(self, rows=ROWS, cols=COLS):
        # Each Boolean layer describes one part of the game state.
        self.layers = np.zeros((3, rows, cols), dtype=bool)
        territory = self.layers[TERRITORY_LAYER]
        territory[0, :] = True
        territory[-1, :] = True
        territory[:, 0] = True
        territory[:, -1] = True
        self.layers[PLAYER_LAYER, 0, cols // 2] = True


class InputController:
    def get_actions(self):
        actions = {"quit": False}

        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True

        return actions


class GameLogic:
    def step(self, model, actions):
        # Movement and capture rules will be added in later steps.
        pass


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
            pg.draw.line(grid, GRID_COLOR, (0, y), (width - 1, y), 1)
        for x in range(0, width, self.cell_size):
            pg.draw.line(grid, GRID_COLOR, (x, 0), (x, height - 1), 1)

        pg.draw.rect(grid, GRID_COLOR, (0, 0, width, height), 1)
        return grid

    def draw(self, layers):
        # Assignment order controls which layer is visible on top.
        cells = np.zeros(layers.shape[1:], dtype=np.uint8)
        cells[layers[TERRITORY_LAYER]] = 1
        cells[layers[TRAIL_LAYER]] = 2
        cells[layers[PLAYER_LAYER]] = 3

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

        rows, cols = self.model.layers.shape[1:]
        self.screen = pg.display.set_mode(
            (cols * CELL_SIZE, rows * CELL_SIZE)
        )
        pg.display.set_caption("Matrix Xonix - Skeleton")

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
                self.view.draw(self.model.layers)
                pg.display.flip()

        pg.quit()


app = GameApp()
app.run()
