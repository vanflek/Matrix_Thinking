import pygame as pg
import numpy as np


ROWS = 20
COLS = 31
CELL_SIZE = 32
FPS = 50
ENEMY_PERIOD = 12

PLAYER_LAYER = 0
BULLET_LAYER = 1
ENEMIES_LAYER = 2
ENEMY_BULLET_LAYER = 3

COLORS = np.array([
    [255, 255, 255],  # Background
    [225, 75, 72],    # Player
    [39, 173, 103],   # Player bullet
    [55, 126, 209],   # Enemies
    [171, 81, 172],   # Enemy bullet
], dtype=np.uint8)
GRID_COLOR = (206, 219, 227)


class GameModel:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.layers = np.zeros((4, rows, cols), dtype=np.uint8)
        self.layers[PLAYER_LAYER, rows - 1, cols // 2] = 1
        # Start with a simple formation; different patterns come later.
        self.layers[ENEMIES_LAYER, 1:4, 1:cols - 1:2] = 1
        self.shooting_permission = True
        self.game_over = False
        self.enemy_direction = "RIGHT"
        self.enemy_tick = 0
        self.enemy_period = ENEMY_PERIOD


class InputController:
    def get_actions(self):
        actions = {
            "move_left": False,
            "move_right": False,
            "move_up": False,
            "move_down": False,
            "shoot": False,
            "quit": False,
        }
        key_actions = {
            pg.K_LEFT: "move_left",
            pg.K_RIGHT: "move_right",
            pg.K_UP: "move_up",
            pg.K_DOWN: "move_down",
            pg.K_SPACE: "shoot",
        }
        action = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True
                elif event.key in key_actions and action is None:
                    action = key_actions[event.key]
        if action is not None:
            actions[action] = True
        return actions


class GameLogic:
    def step(self, model, actions):
        self.apply_action(model, actions)
        self.move_bullet(model)
        self.move_enemies(model)

    def apply_action(self, model, actions):
        player = model.layers[PLAYER_LAYER]
        if actions["move_left"]:
            model.layers[PLAYER_LAYER] = np.roll(player, -1, axis=1)
        elif actions["move_right"]:
            model.layers[PLAYER_LAYER] = np.roll(player, 1, axis=1)
        elif actions["move_up"]:
            model.layers[PLAYER_LAYER] = np.roll(player, -1, axis=0)
        elif actions["move_down"]:
            model.layers[PLAYER_LAYER] = np.roll(player, 1, axis=0)
        elif actions["shoot"] and model.shooting_permission:
            model.layers[BULLET_LAYER] = player
            model.shooting_permission = False

    def move_bullet(self, model):
        if model.shooting_permission:
            return
        bullet = model.layers[BULLET_LAYER]
        # Remove a shot already at the top before a cyclic shift.
        if np.any(bullet[0]):
            bullet[:] = 0
            model.shooting_permission = True
            return
        model.layers[BULLET_LAYER] = np.roll(bullet, -1, axis=0)
        if np.any(model.layers[BULLET_LAYER, 0]):
            model.layers[BULLET_LAYER] = 0
            model.shooting_permission = True

    def shift_no_wrap(self, matrix, direction):
        result = np.zeros_like(matrix)
        if direction == "RIGHT":
            result[:, 1:] = matrix[:, :-1]
        elif direction == "LEFT":
            result[:, :-1] = matrix[:, 1:]
        elif direction == "DOWN":
            result[1:, :] = matrix[:-1, :]
        else:
            result[:] = matrix
        return result

    def move_enemies(self, model):
        model.enemy_tick = (model.enemy_tick + 1) % model.enemy_period
        if model.enemy_tick != 0:
            return

        enemies = model.layers[ENEMIES_LAYER]
        if model.enemy_direction == "RIGHT":
            if np.any(enemies[:, -1]):
                enemies = self.shift_no_wrap(enemies, "DOWN")
                model.enemy_direction = "LEFT"
            else:
                enemies = self.shift_no_wrap(enemies, "RIGHT")
        else:
            if np.any(enemies[:, 0]):
                enemies = self.shift_no_wrap(enemies, "DOWN")
                model.enemy_direction = "RIGHT"
            else:
                enemies = self.shift_no_wrap(enemies, "LEFT")

        model.layers[ENEMIES_LAYER] = enemies
        if np.any(enemies[-1]):
            model.game_over = True


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

    def draw(self, layers):
        player = layers[PLAYER_LAYER]
        bullet = 2 * layers[BULLET_LAYER]
        enemies = 3 * layers[ENEMIES_LAYER]
        enemy_bullet = 4 * layers[ENEMY_BULLET_LAYER]
        cells = np.maximum(np.maximum(player, bullet), enemies)
        cells = np.maximum(cells, enemy_bullet)
        pixels = COLORS[cells]
        pixels = pixels.repeat(self.cell_size, axis=0)
        pixels = pixels.repeat(self.cell_size, axis=1)
        pg.surfarray.blit_array(self.screen, pixels.swapaxes(0, 1))
        self.screen.blit(self.grid, (0, 0))


class GameApp:
    def __init__(self):
        pg.init()
        self.model = GameModel()
        self.controller = InputController()
        self.logic = GameLogic()
        self.screen = pg.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
        pg.display.set_caption("Matrix Invaders - Moving Formation")
        self.view = GameView(self.screen)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running and not self.model.game_over:
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
