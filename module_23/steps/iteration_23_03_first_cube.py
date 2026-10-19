import pygame as pg
import numpy as np


WIDTH, HEIGHT = 1000, 1000
FPS = 60
FOV = np.deg2rad(60)
PROJECTIVE_DISTANCE = WIDTH / (2 * np.tan(FOV / 2))
COLORS = {
    "background": (20, 23, 30),
    "white": (235, 239, 246),
    "muted": (132, 144, 163),
}


class Camera:
    def __init__(self):
        self.position = np.array([1.5, 1.2, -5.0, 1.0])
        self.near = 0.1


class GameModel:
    def __init__(self):
        self.cube_vertices = np.array([
            [0, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 1],
        ], dtype=float)

        self.cube_edges = np.array([
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7],
        ], dtype=np.intp)

        self.objects = {
            "cube": {
                "vertices": self.cube_vertices,
                "edges": self.cube_edges,
                "color": COLORS["white"],
                "screen_lines": np.empty((0, 2, 2)),
            }
        }


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
    def get_camera_vertices(self, camera, vertices):
        camera_vertices = vertices.copy()
        camera_vertices[:, :3] -= camera.position[:3]
        return camera_vertices


    def get_screen_lines(self, camera, vertices, edges):
        camera_vertices = self.get_camera_vertices(camera, vertices)
        if (camera_vertices[:, 2] < camera.near).any():
            return np.empty((0, 2, 2))

        projective_matrix = np.array([
            [PROJECTIVE_DISTANCE, 0, 0, 0],
            [0, PROJECTIVE_DISTANCE, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 0],
        ])
        projected = camera_vertices @ projective_matrix
        w = projected[:, 3]
        screen_x = WIDTH / 2 + projected[:, 0] / w
        screen_y = HEIGHT / 2 - projected[:, 1] / w
        screen_vertices = np.column_stack((screen_x, screen_y))
        return screen_vertices[edges]


class GameView:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Module 23 - 3D wireframe")
        self.font = pg.font.Font(None, 30)

    def draw(self, model):
        self.screen.fill(COLORS["background"])
        for obj in model.objects.values():
            self.draw_object(obj["screen_lines"], obj["color"])

        title = self.font.render(
            "Module 23 | 3D wireframe", True, COLORS["white"]
        )
        self.screen.blit(title, (20, 20))

        help_text = self.font.render(
            "Esc: quit", True, COLORS["muted"]
        )
        self.screen.blit(help_text, (20, HEIGHT - 40))
        pg.display.flip()


    def draw_object(self, lines, color):
        for start, end in lines:
            pg.draw.line(self.screen, color, start, end, 2)


class GameApp:
    def __init__(self):
        pg.init()
        self.model = GameModel()
        self.controller = InputController()
        self.logic = GameLogic()
        self.view = GameView()
        self.camera = Camera()
        self.clock = pg.time.Clock()

    def run(self):
        while True:
            self.clock.tick(FPS)
            actions = self.controller.get_actions()
            if actions["quit"]:
                break

            for obj in self.model.objects.values():
                obj["screen_lines"] = self.logic.get_screen_lines(
                    self.camera, obj["vertices"], obj["edges"]
                )

            self.view.draw(self.model)

        pg.quit()


if __name__ == "__main__":
    game = GameApp()
    game.run()
