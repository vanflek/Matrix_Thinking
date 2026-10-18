import numpy as np
import pygame as pg


ROWS = 32
COLS = 48
CELL_SIZE = 20
FPS = 60
PLAYER_STEP_INTERVAL = 0.02

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
        self.rows = rows
        self.cols = cols
        self.start_position()

    def start_position(self):
        # Rebuild the initial state after a collision.
        self.layers = np.zeros((3, self.rows, self.cols), dtype=bool)
        territory = self.layers[TERRITORY_LAYER]
        territory[0, :] = True
        territory[-1, :] = True
        territory[:, 0] = True
        territory[:, -1] = True
        self.layers[PLAYER_LAYER, 0, self.cols // 2] = True


class InputController:
    def get_actions(self):
        actions = {"quit": False}

        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True

        keys = pg.key.get_pressed()
        actions["move_up"] = keys[pg.K_UP]
        actions["move_down"] = keys[pg.K_DOWN]
        actions["move_left"] = keys[pg.K_LEFT]
        actions["move_right"] = keys[pg.K_RIGHT]
        return actions


class GameLogic:
    def __init__(self):
        self.player_timer = 0.0

    def step(self, model, actions, delta_time):
        self.player_timer += delta_time

        while self.player_timer >= PLAYER_STEP_INTERVAL:
            self.player_timer -= PLAYER_STEP_INTERVAL
            moved = self.player_movement(model, actions)

            if not moved:
                self.player_timer = 0.0
                break

            # Check the OLD trail before marking the new player cell.
            if self.check_suicide(model):
                model.start_position()
                self.player_timer = 0.0
                break

            player = model.layers[PLAYER_LAYER]
            territory = model.layers[TERRITORY_LAYER]
            trail = model.layers[TRAIL_LAYER]
            trail |= player & ~territory

            if (player & territory).any() and trail.any():
                self.captured_area(model)

    def player_movement(self, model, actions):
        if not self.can_move(model, actions):
            return False

        player = model.layers[PLAYER_LAYER]
        if actions["move_up"]:
            model.layers[PLAYER_LAYER] = np.roll(player, -1, axis=0)
        elif actions["move_down"]:
            model.layers[PLAYER_LAYER] = np.roll(player, 1, axis=0)
        elif actions["move_left"]:
            model.layers[PLAYER_LAYER] = np.roll(player, -1, axis=1)
        elif actions["move_right"]:
            model.layers[PLAYER_LAYER] = np.roll(player, 1, axis=1)
        return True

    def can_move(self, model, actions):
        pressed = [actions["move_up"], actions["move_down"],
                   actions["move_left"], actions["move_right"]]
        if np.count_nonzero(pressed) != 1:
            return False

        player = model.layers[PLAYER_LAYER]
        if actions["move_up"] and player[0, :].any():
            return False
        if actions["move_down"] and player[-1, :].any():
            return False
        if actions["move_left"] and player[:, 0].any():
            return False
        if actions["move_right"] and player[:, -1].any():
            return False
        return True

    def check_suicide(self, model):
        return (model.layers[PLAYER_LAYER] & model.layers[TRAIL_LAYER]).any()


    def first_empty_cell(self, blocked):
        for row in range(blocked.shape[0]):
            for col in range(blocked.shape[1]):
                if not blocked[row, col]:
                    return row, col
        return None

    def find_region(self, blocked):
        start = self.first_empty_cell(blocked)
        region = np.zeros_like(blocked)
        if start is None:
            return region

        row, col = start
        region[row, col] = True
        free = ~blocked

        while True:
            # Every direction reads the same previous state.
            previous = region.copy()
            region[1:, :] |= previous[:-1, :]
            region[:-1, :] |= previous[1:, :]
            region[:, 1:] |= previous[:, :-1]
            region[:, :-1] |= previous[:, 1:]
            region &= free

            if np.array_equal(region, previous):
                break

        return region


    def captured_area(self, model):
        territory = model.layers[TERRITORY_LAYER]
        trail = model.layers[TRAIL_LAYER]

        # Commit the line before finding the remaining free regions.
        territory |= trail
        trail[:] = False

        blocked = territory.copy()
        smallest = None
        region_count = 0

        while (~blocked).any():
            region = self.find_region(blocked)
            region_count += 1

            if smallest is None or region.sum() <= smallest.sum():
                smallest = region.copy()

            # Exclude this region from all following searches.
            blocked |= region

        if region_count > 1 and smallest is not None:
            territory |= smallest


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
        pg.display.set_caption("Matrix Xonix - Area capture")

        self.view = GameView(self.screen)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000
            actions = self.controller.get_actions()

            if actions["quit"]:
                self.running = False
            else:
                self.logic.step(self.model, actions, delta_time)
                self.view.draw(self.model.layers)
                pg.display.flip()

        pg.quit()


app = GameApp()

# Examine a small board without changing the live game model.
test_model = GameModel(7, 9)
test_model.layers[TRAIL_LAYER, 1:-1, 3] = True
before = test_model.layers[TERRITORY_LAYER].copy()

blocked = (test_model.layers[TERRITORY_LAYER]
           | test_model.layers[TRAIL_LAYER])
areas = []
while (~blocked).any():
    region = app.logic.find_region(blocked)
    areas.append(int(region.sum()))
    blocked |= region
print("Region areas:", areas)

app.logic.captured_area(test_model)
territory = test_model.layers[TERRITORY_LAYER]
print("New territory cells:", (territory & ~before).sum())
print("Trail empty:", not test_model.layers[TRAIL_LAYER].any())

app.run()
