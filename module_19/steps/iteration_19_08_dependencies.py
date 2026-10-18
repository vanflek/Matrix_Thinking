import numpy as np
import pygame as pg

SCENE_WIDTH = 640
WIDTH = 900
HEIGHT = 480
CELL_SIZE = 40
FPS = 60


class GameModel:
    def __init__(self):
        self._radius = 120.0
        self._angle = 45.0
        self.needs_update = True
        self.cos_value = 1.0
        self.sin_value = 0.0
        self.point = np.zeros(2)
        self.circle_points = np.zeros((360, 2))
        self.graph_angles = np.zeros(361)
        self.sin_values = np.zeros(361)
        self.cos_values = np.zeros(361)


    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        new_radius = max(0.0, value)
        if new_radius != self._radius:
            self._radius = new_radius
            self.needs_update = True

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        new_angle = value % 360
        if new_angle != self._angle:
            self._angle = new_angle
            self.needs_update = True


class InputController:
    def get_actions(self):
        actions = {"quit": False, "angle_delta": 0.0, "radius_delta": 0.0}
        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True
                elif event.key == pg.K_LEFT:
                    actions["angle_delta"] += 1.0
                elif event.key == pg.K_RIGHT:
                    actions["angle_delta"] -= 1.0
                elif event.key == pg.K_UP:
                    actions["radius_delta"] += 5.0
                elif event.key == pg.K_DOWN:
                    actions["radius_delta"] -= 5.0
        return actions


class GameLogic:
    def __init__(self, model):
        self.model = model

        angles = np.deg2rad(np.arange(0.0, 360.0))
        self.unit_circle = np.column_stack((
            np.cos(angles), np.sin(angles),
        ))

        self.model.graph_angles = np.arange(0.0, 361.0)
        graph_radians = np.deg2rad(self.model.graph_angles)
        self.model.sin_values = np.sin(graph_radians)
        self.model.cos_values = np.cos(graph_radians)

        self._calculated_angle = None
        self._calculated_radius = None

    def update(self, actions):
        self.model.angle += actions["angle_delta"]
        self.model.radius += actions["radius_delta"]

        if not self.model.needs_update:
            return

        if self.model.angle != self._calculated_angle:
            radians = np.deg2rad(self.model.angle)
            self.model.cos_value = np.cos(radians)
            self.model.sin_value = np.sin(radians)
            self._calculated_angle = self.model.angle

        if self.model.radius != self._calculated_radius:
            self.model.circle_points = self.model.radius * self.unit_circle
            self._calculated_radius = self.model.radius

        self.model.point = self.model.radius * np.array([
            self.model.cos_value,
            self.model.sin_value,
        ])
        self.model.needs_update = False


class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.font = pg.font.SysFont("Arial", 26)

    def draw_graph(self, label, values, current_value, top, color):
        left = SCENE_WIDTH + 16
        right = WIDTH - 16
        middle_y = top + 58
        amplitude = 22

        title = self.font.render(label, True, color)
        self.screen.blit(title, (left, top))

        graph_x = left + self.model.graph_angles / 360 * (right - left)
        graph_y = middle_y - values * amplitude
        graph_points = np.column_stack((graph_x, graph_y))

        pg.draw.line(self.screen, (170, 180, 190),
                     (left, middle_y), (right, middle_y))
        pg.draw.line(self.screen, (170, 180, 190),
                     (left, middle_y - amplitude),
                     (left, middle_y + amplitude))
        pg.draw.lines(self.screen, color, False, graph_points, 2)

        marker_x = left + self.model.angle / 360 * (right - left)
        marker_y = middle_y - current_value * amplitude
        pg.draw.line(self.screen, (200, 65, 55),
                     (marker_x, middle_y - amplitude),
                     (marker_x, middle_y + amplitude))
        pg.draw.circle(self.screen, (200, 65, 55),
                       (marker_x, marker_y), 4)

    def draw_info_panel(self):
        pg.draw.rect(self.screen, (240, 244, 248),
                     (SCENE_WIDTH, 0, WIDTH - SCENE_WIDTH, HEIGHT))

        point_x, point_y = self.model.point
        lines = [
            "Trigonometry Lab",
            f"Angle: {self.model.angle:.0f} deg",
            f"Radius: {self.model.radius:.0f}",
            f"X: {point_x:.2f}",
            f"Y: {point_y:.2f}",
            f"Cos: {self.model.cos_value:.3f}",
            f"Sin: {self.model.sin_value:.3f}",
        ]

        line_step = self.font.get_linesize() + 6
        for i, text in enumerate(lines):
            image = self.font.render(text, True, (35, 50, 65))
            self.screen.blit(image, (SCENE_WIDTH + 16, 20 + i * line_step))

    def points_to_screen(self, points):
        return np.column_stack((
            SCENE_WIDTH / 2 + points[:, 0],
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

        center = (SCENE_WIDTH // 2, HEIGHT // 2)
        pg.draw.line(self.screen, (110, 120, 130),
                     (0, center[1]), (WIDTH - 1, center[1]), 2)
        pg.draw.line(self.screen, (110, 120, 130),
                     (center[0], 0), (center[0], HEIGHT - 1), 2)

        circle = self.points_to_screen(self.model.circle_points)
        point_x, point_y = self.model.point
        endpoint = (SCENE_WIDTH / 2 + point_x, HEIGHT / 2 - point_y)

        x_projection = (endpoint[0], center[1])
        y_projection = (center[0], endpoint[1])

        pg.draw.lines(self.screen, (0, 130, 155), True, circle, 2)

        pg.draw.line(self.screen, (170, 180, 190),
                     x_projection, endpoint, 1)
        pg.draw.line(self.screen, (170, 180, 190),
                     y_projection, endpoint, 1)

        pg.draw.line(self.screen, (180, 65, 140),
                     center, x_projection, 4)
        pg.draw.line(self.screen, (190, 115, 0),
                     center, y_projection, 4)

        pg.draw.line(self.screen, (45, 90, 180), center, endpoint, 3)
        pg.draw.circle(self.screen, (200, 65, 55), endpoint, 6)
        self.draw_info_panel()
        self.draw_graph("sin(angle)", self.model.sin_values,
                        self.model.sin_value, 285, (190, 115, 0))
        self.draw_graph("cos(angle)", self.model.cos_values,
                        self.model.cos_value, 381, (180, 65, 140))


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
                self.logic.update(actions)
                self.view.draw()
                pg.display.flip()
        pg.quit()


app = GameApp()
app.run()
