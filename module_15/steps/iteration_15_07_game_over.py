import numpy as np
import pygame as pg


ROWS = 20
COLS = 11
CELL_SIZE = 32
FPS = 50
BLOCK_PERIOD = 100

PLAYER_LAYER = 0
BULLET_LAYER = 1
BLOCKS_LAYER = 2

COLORS = np.array([
    [255, 255, 255],  # Background
    [225, 75, 72],    # Player
    [39, 173, 103],   # Bullet
    [55, 126, 209],   # Blocks
], dtype=np.uint8)
GRID_COLOR = (206, 219, 227)


class GameModel:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.layers = np.zeros((3, rows, cols), dtype=np.uint8)
        self.layers[PLAYER_LAYER, rows - 1, cols // 2] = 1
        self.shooting_permission = True
        self.block_tick = 0
        self.block_period = BLOCK_PERIOD
        self.game_over = False


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
        self.check_game_over(model)
        if model.game_over:
            return

        self.move_bullet(model)
        self.resolve_bullet_collision(model)
        self.place_bullet_at_top(model)
        self.check_game_over(model)
        if model.game_over:
            return

        self.move_blocks(model)
        self.resolve_bullet_collision(model)
        self.check_game_over(model)
        if model.game_over:
            return

        self.clear_full_rows(model)
        self.check_game_over(model)

    def apply_action(self, model, actions):
        player = model.layers[PLAYER_LAYER]

        if actions["shoot"] and model.shooting_permission:
            model.layers[BULLET_LAYER] = player
            model.shooting_permission = False
        elif actions["move_left"]:
            model.layers[PLAYER_LAYER] = np.roll(player, -1, axis=1)
        elif actions["move_right"]:
            model.layers[PLAYER_LAYER] = np.roll(player, 1, axis=1)
        elif actions["move_up"]:
            model.layers[PLAYER_LAYER] = np.roll(player, -1, axis=0)
        elif actions["move_down"]:
            model.layers[PLAYER_LAYER] = np.roll(player, 1, axis=0)

    def move_bullet(self, model):
        if model.shooting_permission:
            return

        bullet = model.layers[BULLET_LAYER]
        if bullet[0].any():
            return

        model.layers[BULLET_LAYER] = np.roll(bullet, -1, axis=0)

    def resolve_bullet_collision(self, model):
        bullet = model.layers[BULLET_LAYER]
        blocks = model.layers[BLOCKS_LAYER]
        collision = bullet * blocks
        if not collision.any():
            return

        new_blocks = np.zeros_like(blocks)
        new_blocks[1:] = collision[:-1]
        model.layers[BLOCKS_LAYER] = np.maximum(blocks, new_blocks)
        bullet.fill(0)
        model.shooting_permission = True

    def place_bullet_at_top(self, model):
        bullet = model.layers[BULLET_LAYER]
        if bullet[0].any():
            model.layers[BLOCKS_LAYER, 0] = np.maximum(
                model.layers[BLOCKS_LAYER, 0], bullet[0]
            )
            bullet.fill(0)
            model.shooting_permission = True

    def move_blocks(self, model):
        model.block_tick = (model.block_tick + 1) % model.block_period
        if model.block_tick != 0:
            return

        blocks = model.layers[BLOCKS_LAYER]
        model.layers[BLOCKS_LAYER] = np.roll(blocks, 1, axis=0)
        model.layers[BLOCKS_LAYER, 0] = np.random.randint(
            0, 2, size=model.cols, dtype=np.uint8
        )

    def clear_full_rows(self, model):
        blocks = model.layers[BLOCKS_LAYER]
        full_rows = np.all(blocks == 1, axis=1)
        if not full_rows.any():
            return

        removed = full_rows.sum()
        empty_rows = np.zeros((removed, model.cols), dtype=np.uint8)
        model.layers[BLOCKS_LAYER] = np.vstack((empty_rows, blocks[~full_rows]))

    def check_game_over(self, model):
        player = model.layers[PLAYER_LAYER]
        blocks = model.layers[BLOCKS_LAYER]
        if (player * blocks).any():
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
        blocks = 3 * layers[BLOCKS_LAYER]
        cells = np.maximum(np.maximum(player, bullet), blocks)

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
        pg.display.set_caption("Line Breaker - Skeleton")
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
