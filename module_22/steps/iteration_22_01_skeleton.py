import numpy as np
import pygame as pg

CELL_SIZE = 30
FPS = 60

COLORS = np.array([
    [35, 45, 60],       # Wall: 0.
    [238, 241, 244],    # Passage: 1.
], dtype=np.uint8)

GRID_COLOR = (112, 124, 137)
PLAYER_COLOR = (230, 65, 65)
DIRECTION_COLOR = (42, 117, 170)


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
    def __init__(self, model):
        self.model = model

    def apply_actions(self, actions):
        # Movement actions will be added in the next iteration.
        pass

    def update(self, delta_time):
        # The observer remains stationary in this iteration.
        pass


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

    def draw(self):
        self.screen.blit(self.maze_surface, (0, 0))

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
        self.view = GameView(self.screen, self.model)

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
                self.view.draw()
                pg.display.flip()

        pg.quit()


maze = np.load("maze.npy")
app = GameApp(maze)
app.run()
