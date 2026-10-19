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
    "red": (255, 100, 105),
    "green": (104, 221, 143),
    "blue": (112, 159, 255),
    "cyan": (93, 216, 233),
}


class Camera:
    """Store camera position, angles, and control settings."""
    def __init__(self):
        self.position = np.array([0.0, 1.0, -9.0, 1.0])
        self.near = 0.1
        self.speed = 3.0  # World units per second.
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.mouse_sensitivity = 0.003  # Radians per mouse pixel.
        self.roll_speed = np.deg2rad(45)  # Radians per second.


class GameModel:
    def __init__(self):
        # Cobra Mk III: BBC Micro Elite ship blueprint.
        self.cobra_vertices = np.array([
            [32, 0, 76, 1],
            [-32, 0, 76, 1],
            [0, 26, 24, 1],
            [-120, -3, -8, 1],
            [120, -3, -8, 1],
            [-88, 16, -40, 1],
            [88, 16, -40, 1],
            [128, -8, -40, 1],
            [-128, -8, -40, 1],
            [0, 26, -40, 1],
            [-32, -24, -40, 1],
            [32, -24, -40, 1],
            [-36, 8, -40, 1],
            [-8, 12, -40, 1],
            [8, 12, -40, 1],
            [36, 8, -40, 1],
            [36, -12, -40, 1],
            [8, -16, -40, 1],
            [-8, -16, -40, 1],
            [-36, -12, -40, 1],
            [0, 0, 76, 1],
            [0, 0, 90, 1],
            [-80, -6, -40, 1],
            [-80, 6, -40, 1],
            [-88, 0, -40, 1],
            [80, 6, -40, 1],
            [88, 0, -40, 1],
            [80, -6, -40, 1],
        ], dtype=float)
        self.cobra_edges = np.array([
            [0, 1], [0, 4], [1, 3], [3, 8],
            [4, 7], [6, 7], [6, 9], [5, 9],
            [5, 8], [2, 5], [2, 6], [3, 5],
            [4, 6], [1, 2], [0, 2], [8, 10],
            [10, 11], [7, 11], [1, 10], [0, 11],
            [1, 5], [0, 6], [20, 21], [12, 13],
            [18, 19], [14, 15], [16, 17], [15, 16],
            [14, 17], [13, 18], [12, 19], [2, 9],
            [22, 24], [23, 24], [22, 23], [25, 26],
            [26, 27], [25, 27],
        ], dtype=np.intp)

        self.world_axis_vertices = np.array([
            [0, 0, 0, 1],
            [2, 0, 0, 1],
            [0, 2, 0, 1],
            [0, 0, 2, 1],
        ], dtype=float)
        self.world_axis_edges = np.array([
            [0, 1], [0, 2], [0, 3],
        ], dtype=np.intp)

        self.axis_vertices = np.array([
            [0, 0, 0, 1],
            [1.6, 0, 0, 1],
            [0, 1.6, 0, 1],
            [0, 0, 1.6, 1],
        ], dtype=float)
        self.axis_edges = np.array([
            [0, 1], [0, 2], [0, 3],
        ], dtype=np.intp)
        self.objects = {
            "world": {
                "vertices": self.world_axis_vertices,
                "edges": self.world_axis_edges,
                "position": np.array([0.0, 0.0, 0.0]),
                "initial_angles": np.array([0.0, 0.0, 0.0]),
                "scale": np.array([1.0, 1.0, 1.0]),
                "color": COLORS["muted"],
                "show_axes": False,
                "axis_lines": [],
                "angular_speed": np.array([0.0, 0.0, 0.0]),
                "screen_lines": np.empty((0, 2, 2)),
            },
            "cobra": {
                "vertices": self.cobra_vertices,
                "edges": self.cobra_edges,
                "position": np.array([-2.7, 0.0, 2.0]),
                "initial_angles": np.array([0.25, 0.5, 0.0]),
                "scale": np.array([0.017, 0.017, 0.017]),
                "color": COLORS["white"],
                "show_axes": True,
                "axis_lines": [],
                "angular_speed": np.array([-0.6, 0.0, 0.6]),
                "screen_lines": np.empty((0, 2, 2)),
            },
            "cobra_2": {
                "vertices": self.cobra_vertices,
                "edges": self.cobra_edges,
                "position": np.array([2.7, 0.0, 2.0]),
                "initial_angles": np.array([-0.2, -0.5, 0.1]),
                "scale": np.array([0.014, 0.020, 0.014]),
                "color": COLORS["cyan"],
                "show_axes": True,
                "axis_lines": [],
                "angular_speed": np.array([0.24, 0.0, -0.36]),
                "screen_lines": np.empty((0, 2, 2)),
            },
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
    """Transform geometry and update spatial state."""
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

    def initialize_orientations(self, model):
        for obj in model.objects.values():
            angle_x, angle_y, angle_z = obj["initial_angles"]
            obj["orientation"] = self.get_rotation_matrix(
                angle_x, angle_y, angle_z
            ).T

    def get_world_vertices(self, obj):
        scaling = self.get_scale_matrix(obj["scale"])
        translation = self.get_translation_matrix(obj["position"])
        return (
            obj["vertices"] @ scaling
            @ obj["orientation"] @ translation
        )

    def get_axis_lines(self, camera, obj, axis_vertices, axis_edges):
        translation = self.get_translation_matrix(obj["position"])
        world_axes = axis_vertices @ obj["orientation"] @ translation
        axis_lines = []
        for edge in axis_edges:
            lines = self.get_screen_lines(
                camera, world_axes, np.array([edge])
            )
            axis_lines.append(lines)
        return axis_lines

    def rotate_object(self, obj, angle_x, angle_y, angle_z):
        step = self.get_rotation_matrix(angle_x, angle_y, angle_z).T
        obj["orientation"] = step @ obj["orientation"]

    def animate_objects(self, model, dt):
        for obj in model.objects.values():
            angle_x, angle_y, angle_z = obj["angular_speed"] * dt
            # Intrinsic Z, then X, then Y: each call uses updated local axes.
            self.rotate_object(obj, 0.0, 0.0, angle_z)
            self.rotate_object(obj, angle_x, 0.0, 0.0)
            self.rotate_object(obj, 0.0, angle_y, 0.0)

    def get_scale_matrix(self, scale):
        sx, sy, sz = scale
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1],
        ])


class GameView:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Module 23 - 3D wireframe")
        self.font = pg.font.Font(None, 30)

    def draw(self, model):
        self.screen.fill(COLORS["background"])
        for obj in model.objects.values():
            self.draw_object(obj["screen_lines"], obj["color"])

        for obj in model.objects.values():
            if obj["show_axes"]:
                self.draw_axes(obj["axis_lines"])
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

    def draw_axes(self, axis_lines):
        names = ("X", "Y", "Z")
        colors = (COLORS["red"], COLORS["green"], COLORS["blue"])
        for name, color, lines in zip(names, colors, axis_lines):
            self.draw_object(lines, color)
            if len(lines):
                x, y = lines[0, 1]
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    label = self.font.render(name, True, color)
                    self.screen.blit(label, (round(x) + 5, round(y) + 5))

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
        self.logic.initialize_orientations(self.model)
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
            self.logic.animate_objects(self.model, dt)

            for obj in self.model.objects.values():
                world_vertices = self.logic.get_world_vertices(obj)
                obj["screen_lines"] = self.logic.get_screen_lines(
                    self.camera, world_vertices, obj["edges"]
                )

                if obj["show_axes"]:
                    obj["axis_lines"] = self.logic.get_axis_lines(
                        self.camera, obj,
                        self.model.axis_vertices, self.model.axis_edges
                    )

            self.view.draw(self.model)

        pg.quit()


if __name__ == "__main__":
    game = GameApp()
    game.run()
