import numpy as np
import pygame as pg

WIDTH = 768
HEIGHT = 768
CELL_SIZE = 32
FPS = 60

BACKGROUND_COLOR = (250, 250, 250)
GRID_COLOR = (225, 230, 235)
AXIS_COLOR = (110, 120, 130)
PLAYER_COLOR = (45, 90, 180)


class WireframeObject:
    def __init__(self, vertices, edges, dx=0.0, dy=0.0,
                 sx=1.0, sy=1.0, angle=0.0,
                 color=(0, 0, 0), line_width=2):
        # Each instance owns its local geometry.
        self.vertices = vertices.copy()
        self.edges = edges.copy()

        # Store the position, scale, and orientation of this instance.
        self.dx = dx
        self.dy = dy
        self.sx = sx
        self.sy = sy
        self.angle = angle
        self.color = color
        self.line_width = line_width

    def get_world_vertices(self):
        # Scale the local shape, rotate it, and place it in the world.
        scale_matrix = np.array([
            [self.sx, 0, 0],
            [0, self.sy, 0],
            [0, 0, 1],
        ], dtype=float)

        angle_radians = np.deg2rad(self.angle)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)

        rotation_matrix = np.array([
            [cos_angle, -sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1],
        ], dtype=float)

        translation_matrix = np.array([
            [1, 0, self.dx],
            [0, 1, self.dy],
            [0, 0, 1],
        ], dtype=float)

        transform_matrix = translation_matrix @ rotation_matrix @ scale_matrix
        # Return a new result; keep the local vertices unchanged.
        return self.vertices @ transform_matrix.T


class GameModel:
    def __init__(self):
        # Keep the local geometry from Module 20.
        vertices = np.array([
            [45, 0], [105, 0], [90, 15], [60, 15],
            [0, 90], [-30, 90], [0, 15], [-45, 15],
            [-60, 30], [-75, 30], [-75, -30], [-60, -30],
            [-45, -15], [0, -15], [-30, -90], [0, -90],
            [60, -15], [90, -15], [90, 0], [0, 0],
        ], dtype=float)

        # Add a homogeneous coordinate to every vertex.
        ones = np.ones(len(vertices))
        vertices = np.column_stack((vertices, ones))

        edges = np.array([
            # Outer contour.
            [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
            [6, 7], [7, 8], [8, 9], [9, 10], [10, 11],
            [11, 12], [12, 13], [13, 14], [14, 15],
            [15, 16], [16, 17], [17, 1],
            # Inner wireframe.
            [1, 18], [18, 3], [18, 16], [18, 19],
            [3, 0], [16, 0], [3, 19], [16, 19],
            [6, 13], [19, 6], [19, 13], [7, 12],
        ], dtype=int)

        # The model stores a reference to the player object.
        self.player = WireframeObject(
            vertices=vertices,
            edges=edges,
            dx=0.0,
            dy=0.0,
            sx=1.0,
            sy=1.0,
            angle=90.0,
            color=PLAYER_COLOR,
            line_width=2,
        )

        # A different local shape uses the same vertex and edge format.
        triangle_vertices = np.array([
            [-40, -30, 1],
            [40, -30, 1],
            [0, 50, 1],
        ], dtype=float)
        triangle_edges = np.array([
            [0, 1],
            [1, 2],
            [2, 0],
        ], dtype=int)

        triangle = WireframeObject(
            vertices=triangle_vertices,
            edges=triangle_edges,
            dx=200.0,
            dy=100.0,
            angle=30.0,
            color=(190, 95, 35),
            line_width=3,
        )

        # Store references to both instances for common rendering.
        self.objects = [self.player, triangle]


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
        # Movement actions will be added in a later iteration.
        pass

    def update(self, delta_time):
        # Movement rules will be added in a later iteration.
        pass


class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.grid_surface = self.create_grid_surface()

    def create_grid_surface(self):
        # Draw the fixed background once and reuse it in every frame.
        surface = pg.Surface((WIDTH, HEIGHT))
        surface.fill(BACKGROUND_COLOR)

        for x in range(0, WIDTH, CELL_SIZE):
            pg.draw.line(surface, GRID_COLOR,
                         (x, 0), (x, HEIGHT - 1))
        for y in range(0, HEIGHT, CELL_SIZE):
            pg.draw.line(surface, GRID_COLOR,
                         (0, y), (WIDTH - 1, y))

        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        pg.draw.line(surface, AXIS_COLOR,
                     (0, center_y), (WIDTH - 1, center_y), 2)
        pg.draw.line(surface, AXIS_COLOR,
                     (center_x, 0), (center_x, HEIGHT - 1), 2)
        return surface

    def points_to_screen(self, points):
        # Mathematical Y points up; screen Y points down.
        return np.column_stack((
            WIDTH / 2 + points[:, 0],
            HEIGHT / 2 - points[:, 1],
        ))

    def draw_wireframe(self, game_object):
        # Obtain world coordinates from this particular object.
        world_vertices = game_object.get_world_vertices()
        screen_vertices = self.points_to_screen(world_vertices)

        for start_index, end_index in game_object.edges:
            pg.draw.line(
                self.screen, game_object.color,
                screen_vertices[start_index],
                screen_vertices[end_index], game_object.line_width,
            )

    def draw(self):
        self.screen.blit(self.grid_surface, (0, 0))
        for game_object in self.model.objects:
            self.draw_wireframe(game_object)


class GameApp:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Wireframe Game")
        self.clock = pg.time.Clock()
        self.model = GameModel()
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


app = GameApp()
app.run()
