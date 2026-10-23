import numpy as np
import pygame as pg


ROWS = 32
COLS = 48
CELL_SIZE = 20
FPS = 60
PLAYER_STEP_INTERVAL = 0.02
ENEMY_STEP_INTERVAL = 0.10

TERRITORY_LAYER = 0
TRAIL_LAYER = 1
PLAYER_LAYER = 2
ENEMY_LAYER = 3
GRID_COLOR = (200, 210, 220, 80)

COLORS = np.array([
    [24, 30, 42],     # 0 - free space
    [65, 115, 160],   # 1 - territory
    [245, 185, 60],   # 2 - unfinished trail
    [245, 245, 245],  # 3 - player
    [150, 250, 240],  # 4 - enemy
], dtype=np.uint8)


class GameModel:
    # Store Boolean layers, the level, and one direction vector per enemy.

    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.level = 1
        self.start_position()

    def start_position(self):
        # Every enemy needs a distinct free starting cell.
        capacity = (self.rows - 2) * (self.cols - 2)
        self.enemy_count = min(self.level, capacity)
        self.layers = np.zeros(
            (ENEMY_LAYER + self.enemy_count, self.rows, self.cols),
            dtype=bool
        )

        territory = self.layers[TERRITORY_LAYER]
        territory[0, :] = True
        territory[-1, :] = True
        territory[:, 0] = True
        territory[:, -1] = True
        self.layers[PLAYER_LAYER, 0, self.cols // 2] = True

        # Shuffle complete (row, column) pairs, then select without repeats.
        free_cells = np.argwhere(~territory)
        np.random.shuffle(free_cells)
        for i in range(self.enemy_count):
            row, col = free_cells[i]
            self.layers[ENEMY_LAYER + i, row, col] = True

        directions = np.array([
            [1, 1],
            [1, -1],
            [-1, -1],
            [-1, 1],
        ])
        self.enemy_direction = np.zeros((self.enemy_count, 2), dtype=int)
        for i in range(self.enemy_count):
            self.enemy_direction[i] = directions[i % len(directions)]


class InputController:
    # Combine quit events with the current state of the arrow keys.

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
    # Apply game rules without drawing or changing the window.

    def __init__(self):
        self.player_timer = 0.0
        self.enemy_timer = 0.0

    def step(self, model, actions, delta_time):
        # Advance the enemies independently of player input.
        self.enemy_timer += delta_time
        while self.enemy_timer >= ENEMY_STEP_INTERVAL:
            self.enemy_timer -= ENEMY_STEP_INTERVAL
            self.enemy_move(model)

            if self.check_enemy_collision(model):
                self.restart(model)
                return

        self.player_timer += delta_time
        while self.player_timer >= PLAYER_STEP_INTERVAL:
            self.player_timer -= PLAYER_STEP_INTERVAL
            moved = self.player_movement(model, actions)

            if not moved:
                self.player_timer = 0.0
                break

            # The new position must not overlap the old trail.
            if self.check_suicide(model):
                self.restart(model)
                return

            player = model.layers[PLAYER_LAYER]
            territory = model.layers[TERRITORY_LAYER]
            trail = model.layers[TRAIL_LAYER]
            trail |= player & ~territory

            # A new trail cell can appear at the enemy's current position.
            if self.check_enemy_collision(model):
                self.restart(model)
                return

            if (player & territory).any() and trail.any():
                self.captured_area(model)
                # A completed line can finish the level even without an area.
                if self.check_level_complete(model):
                    model.level += 1
                    self.restart(model)
                    return

    def player_movement(self, model, actions):
        if not self.can_move(model, actions):
            return False

        # Boundary checks have already excluded cyclic wraparound.
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
        # Keep matrix coordinate order: row first, column second.
        for row in range(blocked.shape[0]):
            for col in range(blocked.shape[1]):
                if not blocked[row, col]:
                    return row, col
        return None

    def find_region(self, blocked):
        # Return a new region mask; preserve the input obstacle mask.
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
        enemies = model.layers[ENEMY_LAYER:]

        territory |= trail
        trail[:] = False

        # Track processed regions separately from the actual territory.
        blocked = territory.copy()
        smallest = None
        region_count = 0

        while (~blocked).any():
            region = self.find_region(blocked)
            region_count += 1
            has_enemy = (enemies & region).any()

            if not has_enemy:
                if smallest is None or region.sum() <= smallest.sum():
                    smallest = region.copy()

            # Exclude rejected regions too, so each region is visited once.
            blocked |= region

        if region_count > 1 and smallest is not None:
            territory |= smallest

    def check_level_complete(self, model):
        territory = model.layers[TERRITORY_LAYER][1:-1, 1:-1]
        return territory.sum() >= territory.size * 0.75

    def enemy_step(self, model, i):
        # Calculate a candidate without accepting it yet.
        enemy = model.layers[ENEMY_LAYER + i]
        dy, dx = model.enemy_direction[i]
        candidate = np.roll(enemy, dy, axis=0)
        candidate = np.roll(candidate, dx, axis=1)
        return candidate

    def enemy_move(self, model):
        territory = model.layers[TERRITORY_LAYER]

        for i in range(model.enemy_count):
            layer_index = ENEMY_LAYER + i
            row, col = np.argwhere(model.layers[layer_index])[0]
            dy, dx = model.enemy_direction[i]

            candidate = self.enemy_step(model, i)
            blocked_x = territory[row, col + dx]
            blocked_y = territory[row + dy, col]

            # A free diagonal target is blocked if both side cells are walls.
            if (candidate & territory).any() or (blocked_x and blocked_y):
                if blocked_x:
                    model.enemy_direction[i, 1] *= -1
                if blocked_y:
                    model.enemy_direction[i, 0] *= -1
                if not (blocked_x or blocked_y):
                    model.enemy_direction[i] *= -1

                candidate = self.enemy_step(model, i)

            # Recheck the reflected candidate for this enemy only.
            dy, dx = model.enemy_direction[i]
            corner_blocked = (territory[row, col + dx]
                              and territory[row + dy, col])

            if not (candidate & territory).any() and not corner_blocked:
                model.layers[layer_index] = candidate

    def check_enemy_collision(self, model):
        enemies = model.layers[ENEMY_LAYER:]
        trail = model.layers[TRAIL_LAYER]
        return (enemies & trail).any()

    def restart(self, model):
        # Preserve the level; discard all time left from the previous attempt.
        model.start_position()
        self.player_timer = 0.0
        self.enemy_timer = 0.0


class GameView:
    # Convert masks into an image and overlay the cached grid.

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
        cells = np.zeros(layers.shape[1:], dtype=np.uint8)
        cells[layers[TERRITORY_LAYER]] = 1
        cells[layers[TRAIL_LAYER]] = 2
        for enemy in layers[ENEMY_LAYER:]:
            cells[enemy] = 4
        # Draw the player above the other layers.
        cells[layers[PLAYER_LAYER]] = 3

        pixels = COLORS[cells]
        pixels = np.repeat(pixels, self.cell_size, axis=0)
        pixels = np.repeat(pixels, self.cell_size, axis=1)
        pg.surfarray.blit_array(self.screen, np.swapaxes(pixels, 0, 1))
        self.screen.blit(self.grid, (0, 0))


class GameApp:
    # Connect input, simulation, display, and the frame clock.

    def __init__(self):
        pg.init()
        self.model = GameModel()
        self.controller = InputController()
        self.logic = GameLogic()

        rows, cols = self.model.layers.shape[1:]
        self.screen = pg.display.set_mode(
            (cols * CELL_SIZE, rows * CELL_SIZE)
        )
        pg.display.set_caption(f"Matrix Xonix - Level {self.model.level}")

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
                previous_level = self.model.level
                self.logic.step(self.model, actions, delta_time)

                if self.model.level != previous_level:
                    pg.display.set_caption(
                        f"Matrix Xonix - Level {self.model.level}"
                    )

                self.view.draw(self.model.layers)
                pg.display.flip()

        pg.quit()


app = GameApp()
app.model.level = 6
app.model.start_position()
pg.display.set_caption(f"Matrix Xonix - Level {app.model.level}")
print(app.model.enemy_direction)
app.run()
