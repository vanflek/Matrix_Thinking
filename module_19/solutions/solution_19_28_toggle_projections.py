import numpy as np
import pygame as pg

SCENE_WIDTH = 640
WIDTH = 900
HEIGHT = 480
CELL_SIZE = 40
FPS = 60


class GameModel:
    """Store source parameters and the calculated mathematical state."""
    def __init__(self):
        # Public properties enforce constraints and invalidate derived data.
        self._radius = 120.0
        self._angle = 45.0
        self.show_projections = True
        self.needs_update = True  # Force the initial calculation.
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
    """Translate key events into parameter increments."""
    def get_actions(self):
        actions = {"quit": False, "angle_delta": 0.0, "radius_delta": 0.0, "toggle_projections": False}
        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True
                elif event.key == pg.K_p:
                    actions["toggle_projections"] = not actions["toggle_projections"]
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
    """Calculate dependent values when source parameters change."""
    def __init__(self, model):
        self.model = model

        # Do not repeat the first circle point at 360 degrees.
        angles = np.deg2rad(np.arange(0.0, 360.0))
        self.unit_circle = np.column_stack((
            np.cos(angles), np.sin(angles),
        ))

        # Graphs include both ends of the horizontal angle interval.
        self.model.graph_angles = np.arange(0.0, 361.0)
        graph_radians = np.deg2rad(self.model.graph_angles)
        self.model.sin_values = np.sin(graph_radians)
        self.model.cos_values = np.cos(graph_radians)

        # None distinguishes an absent calculation from a valid zero.
        self._calculated_angle = None
        self._calculated_radius = None

    def update(self, actions):
        if actions["toggle_projections"]:
            self.model.show_projections = not self.model.show_projections
        self.model.angle += actions["angle_delta"]
        self.model.radius += actions["radius_delta"]

        # Apply actions before checking the flag: setters may change it.
        if not self.model.needs_update:
            return

        if self.model.angle != self._calculated_angle:
            radians = np.deg2rad(self.model.angle)
            self.model.cos_value = np.cos(radians)
            self.model.sin_value = np.sin(radians)
            self._calculated_angle = self.model.angle

        # A change of angle does not change the circle.
        if self.model.radius != self._calculated_radius:
            self.model.circle_points = self.model.radius * self.unit_circle
            self._calculated_radius = self.model.radius

        # The endpoint depends on both length and direction.
        self.model.point = self.model.radius * np.array([
            self.model.cos_value,
            self.model.sin_value,
        ])
        self.model.needs_update = False


class GameView:
    """Convert mathematical coordinates and compose each frame."""
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.font = pg.font.SysFont("Arial", 26)
        self.tick_font = pg.font.SysFont("Arial", 14)
        # Cache images that depend only on the fixed layout and graph data.
        self.background = self.create_background()
        self.sin_base = self.create_graph_base(
            "sin(angle)", self.model.sin_values, (190, 115, 0))
        self.cos_base = self.create_graph_base(
            "cos(angle)", self.model.cos_values, (180, 65, 140))

    def create_background(self):
        surface = pg.Surface((WIDTH, HEIGHT))
        surface.fill((250, 250, 250))
        for x in range(0, WIDTH, CELL_SIZE):
            pg.draw.line(surface, (225, 230, 235),
                         (x, 0), (x, HEIGHT - 1))
        for y in range(0, HEIGHT, CELL_SIZE):
            pg.draw.line(surface, (225, 230, 235),
                         (0, y), (WIDTH - 1, y))

        center = (SCENE_WIDTH // 2, HEIGHT // 2)
        pg.draw.line(surface, (110, 120, 130),
                     (0, center[1]), (WIDTH - 1, center[1]), 2)
        pg.draw.line(surface, (110, 120, 130),
                     (center[0], 0), (center[0], HEIGHT - 1), 2)

        return surface

    def create_graph_base(self, label, values, color):
        width = WIDTH - SCENE_WIDTH - 32
        surface = pg.Surface((width + 1, 94))
        surface.fill((240, 244, 248))
        title = self.font.render(label, True, color)
        surface.blit(title, (0, 0))

        plot_left = 22
        plot_width = width - plot_left
        middle_y = 52
        amplitude = 18
        graph_x = plot_left + self.model.graph_angles / 360 * plot_width
        graph_y = middle_y - values * amplitude
        points = np.column_stack((graph_x, graph_y))

        pg.draw.line(surface, (170, 180, 190),
                     (plot_left, middle_y), (width, middle_y))
        pg.draw.line(surface, (170, 180, 190),
                     (plot_left, middle_y - amplitude),
                     (plot_left, middle_y + amplitude))
        pg.draw.lines(surface, color, False, points, 2)

        # Tick labels belong to the reusable graph base.
        for value in [-1, 0, 1]:
            image = self.tick_font.render(str(value), True, (60, 70, 80))
            y = middle_y - value * amplitude - image.get_height() / 2
            surface.blit(image, (0, y))
        for angle in [0, 180, 360]:
            image = self.tick_font.render(f"{angle} deg", True, (60, 70, 80))
            x = plot_left + angle / 360 * plot_width
            if angle == 180:
                x -= image.get_width() / 2
            elif angle == 360:
                x -= image.get_width()
            surface.blit(image, (x, 74))
        return surface

    def draw_graph(self, base, current_value, top):
        # Copy before drawing so markers never accumulate on the base.
        surface = base.copy()
        plot_left = 22
        plot_width = surface.get_width() - 1 - plot_left
        marker_x = plot_left + self.model.angle / 360 * plot_width
        marker_y = 52 - current_value * 18
        pg.draw.line(surface, (200, 65, 55),
                     (marker_x, 34), (marker_x, 70))
        pg.draw.circle(surface, (200, 65, 55),
                       (marker_x, marker_y), 4)
        self.screen.blit(surface, (SCENE_WIDTH + 16, top))

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
        # X points right in both systems; mathematical Y points up.
        return np.column_stack((
            SCENE_WIDTH / 2 + points[:, 0],
            HEIGHT / 2 - points[:, 1],
        ))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        center = (SCENE_WIDTH // 2, HEIGHT // 2)

        circle = self.points_to_screen(self.model.circle_points)
        point_x, point_y = self.model.point
        endpoint = (SCENE_WIDTH / 2 + point_x, HEIGHT / 2 - point_y)

        x_projection = (endpoint[0], center[1])
        y_projection = (center[0], endpoint[1])

        pg.draw.lines(self.screen, (0, 130, 155), True, circle, 2)

        if self.model.show_projections:
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
        # Draw the opaque panel after the scene so it stays readable.
        self.draw_info_panel()
        self.draw_graph(self.sin_base, self.model.sin_value, 285)
        self.draw_graph(self.cos_base, self.model.cos_value, 381)


class GameApp:
    """Own components, process frames, and close Pygame."""
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Trigonometry Lab")
        self.clock = pg.time.Clock()
        self.model = GameModel()
        self.controller = InputController()
        # Prepare graph data before the view builds its graph images.
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
