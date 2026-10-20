import numpy as np
import pygame as pg

WIDTH = 640
HEIGHT = 480
CELL_SIZE = 40
FPS = 60
MOVE_STEP = 10.0
ANGLE_STEP = 5.0
SCALE_STEP = 0.25


class GameModel:
    def __init__(self):
        # Mathematical coordinates of the house vertices: [x, y].
        self.vertices = np.array([
            [-60, -40], [60, -40], [60, 40],
            [0, 90], [-60, 40],
        ], dtype=float)

        # Add the homogeneous coordinate to every vertex.
        ones = np.ones(len(self.vertices))
        self.vertices = np.column_stack((self.vertices, ones))

        # Displacement from the original placement, in mathematical units.
        self.dx = 0.0
        self.dy = 0.0

        # Independent scale factors for the local X and Y axes.
        self.sx = 1.0
        self.sy = 1.0
        self.angle = 0.0
        self.marked_vertex_index = 3
        self.transformed_vertices = self.vertices.copy()

        # The first group closes the outline; the second adds inner lines.
        self.edges = np.array([
            [0, 1], [1, 2], [2, 3],
            [3, 4], [4, 0], [2, 4],
        ], dtype=int)


class InputController:
    def get_actions(self):
        actions = {
            "quit": False,
            "move_x": 0, "move_y": 0,
            "turn": 0,
            "scale_x": 0, "scale_y": 0,
            "reset": False,
        }
        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True
                elif event.key == pg.K_LEFT:
                    actions["move_x"] -= 1
                elif event.key == pg.K_RIGHT:
                    actions["move_x"] += 1
                elif event.key == pg.K_UP:
                    actions["move_y"] += 1
                elif event.key == pg.K_DOWN:
                    actions["move_y"] -= 1
                elif event.key == pg.K_q:
                    actions["turn"] += 1
                elif event.key == pg.K_e:
                    actions["turn"] -= 1
                elif event.key == pg.K_a:
                    actions["scale_x"] -= 1
                elif event.key == pg.K_d:
                    actions["scale_x"] += 1
                elif event.key == pg.K_s:
                    actions["scale_y"] -= 1
                elif event.key == pg.K_w:
                    actions["scale_y"] += 1
                elif event.key == pg.K_r:
                    actions["reset"] = True
        return actions


class GameLogic:
    def __init__(self, model):
        self.model = model

    def apply_actions(self, actions):
        # Reset takes priority over other parameter changes in this frame.
        if actions["reset"]:
            self.model.dx = 0.0
            self.model.dy = 0.0
            self.model.angle = 0.0
            self.model.sx = 1.0
            self.model.sy = 1.0
            return

        self.model.dx += actions["move_x"] * MOVE_STEP
        self.model.dy += actions["move_y"] * MOVE_STEP
        self.model.angle += actions["turn"] * ANGLE_STEP
        self.model.sx += actions["scale_x"] * SCALE_STEP
        self.model.sy += actions["scale_y"] * SCALE_STEP

    def update(self):
        # Scale the original shape around the local origin.
        scale_matrix = np.array([
            [self.model.sx, 0, 0],
            [0, self.model.sy, 0],
            [0, 0, 1],
        ], dtype=float)

        # Rotate the scaled shape. The model stores the angle in degrees.
        angle_radians = np.deg2rad(self.model.angle)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)

        rotation_matrix = np.array([
            [cos_angle, -sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1],
        ], dtype=float)

        # Place the rotated shape in the scene.
        translation_matrix = np.array([
            [1, 0, self.model.dx],
            [0, 1, self.model.dy],
            [0, 0, 1],
        ], dtype=float)
        # Compose local scaling, local rotation, and world translation.
        transform_matrix = translation_matrix @ rotation_matrix @ scale_matrix
        # Vertices are stored as rows, so transpose the combined matrix.
        self.model.transformed_vertices = (
            self.model.vertices @ transform_matrix.T
        )


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
        screen_vertices = self.points_to_screen(
            self.model.transformed_vertices
        )
        self.draw_wireframe(screen_vertices, self.model.edges)

        # Mark vertices to make the structure of the wireframe visible.
        for point in screen_vertices:
            pg.draw.circle(self.screen, (200, 65, 55), point, 5)

        # Mark one vertex so that reflections of symmetric shapes are visible.
        marked_point = screen_vertices[self.model.marked_vertex_index]
        pg.draw.circle(self.screen, (170, 65, 150), marked_point, 7)


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
                self.logic.apply_actions(actions)
                self.logic.update()
                self.view.draw()
                pg.display.flip()
        pg.quit()


app = GameApp()
app.run()
