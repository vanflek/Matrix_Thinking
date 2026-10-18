import numpy as np
import pygame as pg

WIDTH = 640
HEIGHT = 480
CELL_SIZE = 40
FPS = 60


class GameModel:
    def __init__(self):
        self.radius = 120.0
        self.angle = 45.0
        self.point = np.zeros(2)
        self.circle_points = np.zeros((360, 2))


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

    def update(self):
        angle_radians = np.deg2rad(self.model.angle)
        self.model.point = self.model.radius * np.array([
            np.cos(angle_radians),
            np.sin(angle_radians),
        ])

        angles = np.deg2rad(np.arange(0.0, 360.0))
        self.model.circle_points = self.model.radius * np.column_stack((
            np.cos(angles), np.sin(angles),
        ))


class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model

    def points_to_screen(self, points):
        return np.column_stack((
            WIDTH / 2 + points[:, 0],
            HEIGHT / 2 - points[:, 1],
        ))

    def draw(self):
        self.screen.fill((250, 250, 250))
        for x in range(0, WIDTH, CELL_SIZE):
            pg.draw.line(self.screen, (225, 230, 235),
                         (x, 0), (x, HEIGHT - 1))
        for y in range(0, HEIGHT, CELL_SIZE):
            pg.draw.line(self.screen, (225, 230, 235),
                         (0, y), (WIDTH - 1, y))

        center = (WIDTH // 2, HEIGHT // 2)
        pg.draw.line(self.screen, (110, 120, 130),
                     (0, center[1]), (WIDTH - 1, center[1]), 2)
        pg.draw.line(self.screen, (110, 120, 130),
                     (center[0], 0), (center[0], HEIGHT - 1), 2)

        circle = self.points_to_screen(self.model.circle_points)
        point_x, point_y = self.model.point
        endpoint = (WIDTH / 2 + point_x, HEIGHT / 2 - point_y)

        pg.draw.lines(self.screen, (0, 130, 155), True, circle, 2)
        pg.draw.line(self.screen, (45, 90, 180), center, endpoint, 3)
        pg.draw.circle(self.screen, (200, 65, 55), endpoint, 6)


class GameApp:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Trigonometry Lab")
        self.clock = pg.time.Clock()
        self.model = GameModel()
        self.controller = InputController()
        self.logic = GameLogic(self.model)
        self.view = GameView(self.screen, self.model)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            actions = self.controller.get_actions()
            if actions["quit"]:
                running = False
            else:
                self.logic.update()
                self.view.draw()
                pg.display.flip()
        pg.quit()


app = GameApp()
app.run()
