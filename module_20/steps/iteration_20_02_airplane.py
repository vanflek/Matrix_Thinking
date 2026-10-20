import numpy as np
import pygame as pg

WIDTH = 640
HEIGHT = 480
CELL_SIZE = 40
FPS = 60


class GameModel:
    def __init__(self):
        # Mathematical coordinates of the airplane vertices: [x, y].
        self.vertices = np.array([
            [45, 0],      # 0 body reference point
            [105, 0],     # 1 nose
            [90, 15],     # 2 upper front body
            [60, 15],     # 3 upper body
            [0, 90],      # 4 upper wing front outer
            [-30, 90],    # 5 upper wing rear outer
            [0, 15],      # 6 upper wing root
            [-45, 15],    # 7 upper tail body
            [-60, 30],    # 8 upper tail front outer
            [-75, 30],    # 9 upper tail rear outer
            [-75, -30],   # 10 lower tail rear outer
            [-60, -30],   # 11 lower tail front outer
            [-45, -15],   # 12 lower tail body
            [0, -15],     # 13 lower wing root
            [-30, -90],   # 14 lower wing rear outer
            [0, -90],     # 15 lower wing front outer
            [60, -15],    # 16 lower body
            [90, -15],    # 17 lower front body
            [90, 0],      # 18 cockpit
            [0, 0],       # 19 local origin
        ], dtype=float)

        # The first group closes the outline; the second adds inner lines.
        self.edges = np.array([
            # Outer contour
            [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
            [6, 7], [7, 8], [8, 9], [9, 10], [10, 11],
            [11, 12], [12, 13], [13, 14], [14, 15],
            [15, 16], [16, 17], [17, 1],

            # Inner wireframe
            [1, 18], [18, 3], [18, 16], [18, 19],
            [3, 0], [16, 0], [3, 19], [16, 19],
            [6, 13], [19, 6], [19, 13], [7, 12],
        ], dtype=int)


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
        # Transformations will be added in the following steps.
        pass


class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.grid_surface = self.create_grid_surface()

    def create_grid_surface(self):
        surface = pg.Surface((WIDTH, HEIGHT))
        surface.fill((250, 250, 250))

        for x in range(0, WIDTH, CELL_SIZE):
            pg.draw.line(surface, (225, 230, 235),
                         (x, 0), (x, HEIGHT - 1))
        for y in range(0, HEIGHT, CELL_SIZE):
            pg.draw.line(surface, (225, 230, 235),
                         (0, y), (WIDTH - 1, y))

        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        pg.draw.line(surface, (110, 120, 130),
                     (0, center_y), (WIDTH - 1, center_y), 2)
        pg.draw.line(surface, (110, 120, 130),
                     (center_x, 0), (center_x, HEIGHT - 1), 2)
        return surface

    def points_to_screen(self, points):
        # Mathematical Y points up; screen Y points down.
        return np.column_stack((
            WIDTH / 2 + points[:, 0],
            HEIGHT / 2 - points[:, 1],
        ))

    def draw_wireframe(self, screen_vertices, edges):
        for start_index, end_index in edges:
            start_point = screen_vertices[start_index]
            end_point = screen_vertices[end_index]
            pg.draw.line(self.screen, (45, 90, 180),
                         start_point, end_point, 3)

    def draw(self):
        self.screen.blit(self.grid_surface, (0, 0))
        screen_vertices = self.points_to_screen(self.model.vertices)
        self.draw_wireframe(screen_vertices, self.model.edges)

        # Mark vertices to make the structure of the wireframe visible.
        for point in screen_vertices:
            pg.draw.circle(self.screen, (200, 65, 55), point, 5)


class GameApp:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Affine Transformations")
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
