import numpy as np
import pygame as pg

CELL_SIZE = 30
FPS = 60
MOUSE_SENSITIVITY = 0.003

COLORS = np.array([
    [35, 45, 60],       # Wall: 0.
    [238, 241, 244],    # Passage: 1.
], dtype=np.uint8)

GRID_COLOR = (112, 124, 137)
PLAYER_COLOR = (230, 65, 65)
DIRECTION_COLOR = (42, 117, 170)
RAY_COLOR = (0, 145, 155)
SAMPLE_COLOR = (230, 151, 48)
WALL_SAMPLE_COLOR = (220, 80, 150)


class GameModel:
    def __init__(self, maze):
        self.maze = maze
        self.rows, self.columns = maze.shape
        self.world_height = self.rows * CELL_SIZE
        self.world_width = self.columns * CELL_SIZE

        # This interior passage belongs to the supplied maze.npy.
        start_row, start_column = 8, 16
        assert maze[start_row, start_column] == 1

        # Store the observer's coordinates in the order [y, x].
        self.player_position = np.array([
            start_row + 0.5, start_column + 0.5
        ]) * CELL_SIZE
        self.player_angle = 0.0
        self.player_speed = 90.0


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
        actions["forward"] = keys[pg.K_w]
        actions["backward"] = keys[pg.K_s]
        actions["left"] = keys[pg.K_a]
        actions["right"] = keys[pg.K_d]
        actions["mouse_dx"] = pg.mouse.get_rel()[0]
        return actions


class GameLogic:
    def __init__(self, model):
        self.model = model
        self.actions = {}

    def apply_actions(self, actions):
        self.actions = actions

    def update(self, delta_time):
        # Mouse input is already a displacement, not a speed.
        self.model.player_angle += (
            self.actions["mouse_dx"] * MOUSE_SENSITIVITY
        )
        self.model.player_angle %= 2 * np.pi

        angle = self.model.player_angle
        # Both vectors use the coordinate order [y, x].
        forward = np.array([np.sin(angle), np.cos(angle)])
        right = np.array([np.cos(angle), -np.sin(angle)])

        movement = np.zeros(2, dtype=float)
        if self.actions["forward"]:
            movement += forward
        if self.actions["backward"]:
            movement -= forward
        if self.actions["right"]:
            movement += right
        if self.actions["left"]:
            movement -= right

        length = np.linalg.norm(movement)
        if length == 0:
            return

        direction = movement / length
        distance = self.model.player_speed * delta_time

        # Check short, axis-aligned moves to avoid skipping a wall.
        max_step = CELL_SIZE / 4
        step_count = int(distance / max_step) + 1
        step = direction * distance / step_count

        for _ in range(step_count):
            for axis in range(2):
                candidate = self.model.player_position.copy()
                candidate[axis] += step[axis]
                if self.can_move(candidate):
                    self.model.player_position = candidate

    def can_move(self, position):
        y, x = position
        # Validate world coordinates before indexing the matrix.
        if not (0 <= y < self.model.world_height
                and 0 <= x < self.model.world_width):
            return False

        row = int(y // CELL_SIZE)
        column = int(x // CELL_SIZE)
        return self.model.maze[row, column] == 1


class RayCaster:
    def __init__(self, model):
        self.model = model
        self.fov = np.deg2rad(60)
        self.rays_count = 9
        self.sample_count = 31

        # The map diagonal bounds distances between points in the map.
        self.ray_length = np.linalg.norm([
            model.world_height, model.world_width
        ])
        self.relative_angles = np.linspace(
            -self.fov / 2, self.fov / 2, self.rays_count
        )
        self.distances = np.linspace(
            0, self.ray_length, self.sample_count
        )

    def ray_cast(self):
        ray_angles = self.model.player_angle + self.relative_angles
        angle_grid, distance_grid = np.meshgrid(
            ray_angles, self.distances
        )

        player_y, player_x = self.model.player_position
        ray_y = player_y + distance_grid * np.sin(angle_grid)
        ray_x = player_x + distance_grid * np.cos(angle_grid)

        cell_y = (ray_y // CELL_SIZE).astype(int)
        cell_x = (ray_x // CELL_SIZE).astype(int)
        inside = (
            (cell_y >= 0) & (cell_y < self.model.rows) &
            (cell_x >= 0) & (cell_x < self.model.columns)
        )
        walls = np.zeros_like(inside)
        walls[inside] = (
            self.model.maze[cell_y[inside], cell_x[inside]] == 0
        )
        has_wall = walls.any(axis=0)
        return ray_y, ray_x, inside, walls, has_wall


class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.maze_surface = self.create_maze_surface()

    def create_maze_surface(self):
        # Replace each cell value with an RGB vector.
        rgb = COLORS[self.model.maze]
        rgb = np.repeat(rgb, CELL_SIZE, axis=0)
        rgb = np.repeat(rgb, CELL_SIZE, axis=1)
        rgb = np.swapaxes(rgb, 0, 1)
        surface = pg.surfarray.make_surface(rgb)

        # Add the fixed grid once, together with the map.
        width = self.model.world_width
        height = self.model.world_height
        for x in range(0, width, CELL_SIZE):
            pg.draw.line(surface, GRID_COLOR,
                         (x, 0), (x, height - 1))
        for y in range(0, height, CELL_SIZE):
            pg.draw.line(surface, GRID_COLOR,
                         (0, y), (width - 1, y))
        pg.draw.rect(surface, GRID_COLOR, (0, 0, width, height), 1)
        return surface

    def draw_rays(self, ray_y, ray_x, walls):
        player_y, player_x = self.model.player_position
        for ray_index in range(ray_x.shape[1]):
            end_y = ray_y[-1, ray_index]
            end_x = ray_x[-1, ray_index]
            pg.draw.line(
                self.screen, RAY_COLOR,
                (player_x, player_y), (end_x, end_y), 1,
            )
            for sample_index in range(ray_x.shape[0]):
                y = ray_y[sample_index, ray_index]
                x = ray_x[sample_index, ray_index]
                color = SAMPLE_COLOR
                if walls[sample_index, ray_index]:
                    color = WALL_SAMPLE_COLOR
                pg.draw.circle(self.screen, color, (x, y), 2)

    def draw(self, ray_y, ray_x, walls):
        self.screen.blit(self.maze_surface, (0, 0))
        self.draw_rays(ray_y, ray_x, walls)

        player_y, player_x = self.model.player_position
        angle = self.model.player_angle
        end_x = player_x + 20 * np.cos(angle)
        end_y = player_y + 20 * np.sin(angle)

        pg.draw.line(
            self.screen, DIRECTION_COLOR,
            (player_x, player_y), (end_x, end_y), 2,
        )
        pg.draw.circle(
            self.screen, PLAYER_COLOR, (player_x, player_y), 5,
        )


class GameApp:
    def __init__(self, maze):
        pg.init()
        self.model = GameModel(maze)
        # The first window shows the map at one pixel per world unit.
        self.screen = pg.display.set_mode((
            self.model.world_width, self.model.world_height
        ))
        pg.display.set_caption("Raycasting: map and observer")
        self.clock = pg.time.Clock()
        self.controller = InputController()
        self.logic = GameLogic(self.model)
        self.ray_caster = RayCaster(self.model)
        self.view = GameView(self.screen, self.model)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.mouse.get_rel()  # Discard motion accumulated during setup.

    def run(self):
        running = True
        while running:
            delta_time = self.clock.tick(FPS) / 1000
            actions = self.controller.get_actions()

            if actions["quit"]:
                running = False
            else:
                self.logic.apply_actions(actions)
                self.logic.update(delta_time)
                result = self.ray_caster.ray_cast()
                ray_y, ray_x, inside, walls, has_wall = result
                pg.display.set_caption(
                    f"Raycasting: {has_wall.sum()} / {has_wall.size} rays hit walls"
                )
                self.view.draw(ray_y, ray_x, walls)
                pg.display.flip()

        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        pg.quit()


maze = np.load("maze.npy")
app = GameApp(maze)
app.run()
