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
        self.speed = 3.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.mouse_sensitivity = 0.003
        self.roll_speed = np.deg2rad(45)


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

        self.cube_vertices[:, :3] -= 0.5

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
                "position": np.array([0.0, 0.0, 0.0]),
                "initial_angles": np.array([0.25, 0.5, 0.0]),
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

        keys = pg.key.get_pressed()
        actions["forward"] = keys[pg.K_w]
        actions["backward"] = keys[pg.K_s]
        actions["left"] = keys[pg.K_a]
        actions["right"] = keys[pg.K_d]
        actions["up"] = keys[pg.K_SPACE]
        actions["down"] = keys[pg.K_LCTRL]
        actions["roll_positive"] = keys[pg.K_q]
        actions["roll_negative"] = keys[pg.K_e]
        actions["mouse_dx"], actions["mouse_dy"] = pg.mouse.get_rel()
        return actions


class GameLogic:
    def get_camera_vertices(self, camera, vertices):
        camera_vertices = vertices.copy()
        camera_vertices[:, :3] -= camera.position[:3]
        rotation = self.get_rotation_matrix(
            camera.pitch, camera.yaw, camera.roll
        )
        return camera_vertices @ rotation


    def get_screen_lines(self, camera, vertices, edges):
        camera_vertices = self.get_camera_vertices(camera, vertices)
        lines = camera_vertices[edges]
        lines = self.clip_lines(lines, camera.near)

        projective_matrix = np.array([
            [PROJECTIVE_DISTANCE, 0, 0, 0],
            [0, PROJECTIVE_DISTANCE, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 0],
        ])
        projected = lines @ projective_matrix
        w = projected[:, :, 3]
        screen_x = WIDTH / 2 + projected[:, :, 0] / w
        screen_y = HEIGHT / 2 - projected[:, :, 1] / w
        return np.stack((screen_x, screen_y), axis=2)


    def camera_move(self, camera, actions, dt):
        movement_camera = np.array([
            actions["right"] - actions["left"],
            actions["up"] - actions["down"],
            actions["forward"] - actions["backward"],
            0,
        ], dtype=float)
        length = np.linalg.norm(movement_camera)
        if length > 0:
            movement_camera = (
                movement_camera / length * camera.speed * dt
            )

        rotation = self.get_rotation_matrix(
            camera.pitch, camera.yaw, camera.roll
        )
        movement_world = movement_camera @ rotation.T
        translation = self.get_translation_matrix(movement_world[:3])
        camera.position = camera.position @ translation

    def get_translation_matrix(self, position):
        dx, dy, dz = position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dx, dy, dz, 1],
        ])


    def camera_rotate(self, camera, actions, dt):
        camera.yaw += actions["mouse_dx"] * camera.mouse_sensitivity
        camera.pitch -= actions["mouse_dy"] * camera.mouse_sensitivity
        camera.roll += (
            (actions["roll_positive"] - actions["roll_negative"])
            * camera.roll_speed * dt
        )

    def get_rotation_matrix(self, angle_x, angle_y, angle_z):
        cos_y = np.cos(angle_y)
        sin_y = np.sin(angle_y)
        cos_x = np.cos(angle_x)
        sin_x = np.sin(angle_x)
        cos_z = np.cos(angle_z)
        sin_z = np.sin(angle_z)
        rotation_y = np.array([
            [cos_y, 0, sin_y, 0],
            [0, 1, 0, 0],
            [-sin_y, 0, cos_y, 0],
            [0, 0, 0, 1],
        ])
        rotation_x = np.array([
            [1, 0, 0, 0],
            [0, cos_x, sin_x, 0],
            [0, -sin_x, cos_x, 0],
            [0, 0, 0, 1],
        ])
        rotation_z = np.array([
            [cos_z, sin_z, 0, 0],
            [-sin_z, cos_z, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        return rotation_y @ rotation_x @ rotation_z


    def clip_lines(self, lines, near):
        depths = lines[:, :, 2]
        keep = (depths >= near).any(axis=1)
        lines = lines[keep]

        for end in range(2):
            other = 1 - end
            behind = lines[:, end, 2] < near
            start_points = lines[behind, end]
            end_points = lines[behind, other]
            t = (
                (near - start_points[:, 2])
                / (end_points[:, 2] - start_points[:, 2])
            )
            lines[behind, end] = (
                start_points + t[:, None] * (end_points - start_points)
            )
            lines[behind, end, 2] = near

        return lines


    def get_world_vertices(self, obj):
        angle_x, angle_y, angle_z = obj["initial_angles"]
        orientation = self.get_rotation_matrix(
            angle_x, angle_y, angle_z
        ).T
        translation = self.get_translation_matrix(obj["position"])
        return obj["vertices"] @ orientation @ translation


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
            "WASD: move | Space/Ctrl: up/down | Mouse: look | Q/E: roll | Esc: quit",
            True, COLORS["muted"]
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
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.mouse.get_rel()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            actions = self.controller.get_actions()
            if actions["quit"]:
                break

            self.logic.camera_rotate(self.camera, actions, dt)
            self.logic.camera_move(self.camera, actions, dt)

            for obj in self.model.objects.values():
                world_vertices = self.logic.get_world_vertices(obj)
                obj["screen_lines"] = self.logic.get_screen_lines(
                    self.camera, world_vertices, obj["edges"]
                )

            self.view.draw(self.model)

        pg.quit()


if __name__ == "__main__":
    game = GameApp()
    game.run()
