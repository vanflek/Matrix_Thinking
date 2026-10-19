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


PROJECTILE_COLOR = (35, 135, 85)

# The projectile points along its local positive X axis.
PROJECTILE_VERTICES = np.array([
    [12, 0, 1],
    [0, 3, 1],
    [-8, 0, 1],
    [0, -3, 1],
], dtype=float)
PROJECTILE_EDGES = np.array([
    [0, 1], [1, 2], [2, 3], [3, 0], [0, 2],
], dtype=int)


ENEMY_COLOR = (185, 65, 45)

# Four ray tips, four inner corners, and the local center.
ENEMY_VERTICES = np.array([
    [30, 0, 1],
    [10, 7.5, 1],
    [0, 30, 1],
    [-7.5, 10, 1],
    [-30, 0, 1],
    [-10, -7.5, 1],
    [0, -30, 1],
    [7.5, -10, 1],
    [0, 0, 1],
], dtype=float)
ENEMY_EDGES = np.array([
    # Outer contour.
    [0, 1], [1, 2], [2, 3], [3, 4],
    [4, 5], [5, 6], [6, 7], [7, 0],
    # Inner wireframe.
    [8, 0], [8, 2], [8, 4], [8, 6],
    [1, 5], [3, 7],
], dtype=int)


class WireframeObject:
    def __init__(self, vertices, edges, dx=0.0, dy=0.0,
                 sx=1.0, sy=1.0, angle=0.0,
                 color=(0, 0, 0), line_width=2,
                 velocity_x=0.0, velocity_y=0.0,
                 angular_speed=0.0, motion_type="static",
                 orbit_center_x=0.0, orbit_center_y=0.0,
                 orbit_radius=0.0, orbit_angle=0.0, orbit_speed=0.0):
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
        # Store world-space velocity components for moving objects.
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.angular_speed = angular_speed
        self.motion_type = motion_type

        # These values describe circular trajectories interpreted by GameLogic.
        self.orbit_center_x = orbit_center_x
        self.orbit_center_y = orbit_center_y
        self.orbit_radius = orbit_radius
        self.orbit_angle = orbit_angle
        self.orbit_speed = orbit_speed

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


    def get_bounding_radius(self):
        scaled_x = self.vertices[:, 0] * self.sx
        scaled_y = self.vertices[:, 1] * self.sy
        return np.max(np.hypot(scaled_x, scaled_y))


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
            dy=-245.0,
            sx=0.5,
            sy=0.5,
            angle=90.0,
            color=PLAYER_COLOR,
            line_width=2,
        )

        # Two enemies move on crossing diagonals.
        self.enemies = []
        self.projectiles = []
        diagonal_data = [
            # Initial X, horizontal velocity, visual spin.
            (-250.0, 120.0, 70.0),
            (250.0, -120.0, -70.0),
        ]
        for dx, velocity_x, angular_speed in diagonal_data:
            enemy = WireframeObject(
                vertices=ENEMY_VERTICES,
                edges=ENEMY_EDGES,
                dx=dx,
                dy=250.0,
                color=ENEMY_COLOR,
                line_width=3,
                velocity_x=velocity_x,
                velocity_y=-120.0,
                angular_speed=angular_speed,
                motion_type="diagonal",
            )
            self.enemies.append(enemy)

        # Four enemies share one circle but have independent phases and spins.
        center_x = 0.0
        center_y = 40.0
        radius = 185.0
        circular_data = [
            # Initial phase, orbital angular speed, visual spin.
            (0.0, 34.0, 65.0),
            (90.0, -34.0, -65.0),
            (180.0, 34.0, 65.0),
            (270.0, -34.0, -65.0),
        ]
        for phase, orbit_speed, angular_speed in circular_data:
            phase_radians = np.deg2rad(phase)
            enemy = WireframeObject(
                vertices=ENEMY_VERTICES,
                edges=ENEMY_EDGES,
                dx=center_x + radius * np.cos(phase_radians),
                dy=center_y + radius * np.sin(phase_radians),
                angle=phase,
                color=ENEMY_COLOR,
                line_width=3,
                angular_speed=angular_speed,
                motion_type="circle",
                orbit_center_x=center_x,
                orbit_center_y=center_y,
                orbit_radius=radius,
                orbit_angle=phase,
                orbit_speed=orbit_speed,
            )
            self.enemies.append(enemy)

    def get_all_objects(self):
        return [self.player, *self.enemies, *self.projectiles]


class InputController:
    def get_actions(self):
        actions = {
            "quit": False,
            "forward": False,
            "backward": False,
            "strafe_left": False,
            "strafe_right": False,
            "turn_left": False,
            "turn_right": False,
            "fire": False,
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions["quit"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    actions["quit"] = True
                elif event.key == pg.K_SPACE:
                    actions["fire"] = True

        # Continuous actions use the current state of the keyboard.
        keys = pg.key.get_pressed()
        actions["forward"] = keys[pg.K_w]
        actions["backward"] = keys[pg.K_s]
        actions["strafe_left"] = keys[pg.K_a]
        actions["strafe_right"] = keys[pg.K_d]
        actions["turn_left"] = keys[pg.K_LEFT]
        actions["turn_right"] = keys[pg.K_RIGHT]
        return actions


class GameLogic:
    def __init__(self, model):
        self.model = model
        self.move_speed = 220.0
        self.turn_speed = 120.0
        self.projectile_speed = 520.0
        self.actions = {
            "forward": False,
            "backward": False,
            "strafe_left": False,
            "strafe_right": False,
            "turn_left": False,
            "turn_right": False,
            "fire": False,
        }

    def apply_actions(self, actions):
        # Remember the actions to apply during this frame's update.
        self.actions = actions

    def update(self, delta_time):
        self.update_player(delta_time)
        if self.actions["fire"]:
            self.create_projectile()
        self.update_projectiles(delta_time)
        self.update_enemies(delta_time)

    def update_player(self, delta_time):
        player = self.model.player
        actions = self.actions

        # Rotate first, then use the resulting orientation for movement.
        if actions["turn_left"]:
            player.angle += self.turn_speed * delta_time
        if actions["turn_right"]:
            player.angle -= self.turn_speed * delta_time
        player.angle %= 360

        angle_radians = np.deg2rad(player.angle)
        forward_x = np.cos(angle_radians)
        forward_y = np.sin(angle_radians)
        left_x = -forward_y
        left_y = forward_x

        move_x = 0.0
        move_y = 0.0
        if actions["forward"]:
            move_x += forward_x
            move_y += forward_y
        if actions["backward"]:
            move_x -= forward_x
            move_y -= forward_y
        if actions["strafe_left"]:
            move_x += left_x
            move_y += left_y
        if actions["strafe_right"]:
            move_x -= left_x
            move_y -= left_y

        # Keep one movement speed when combining perpendicular directions.
        length = np.hypot(move_x, move_y)
        if length > 0:
            move_x /= length
            move_y /= length
            distance = self.move_speed * delta_time
            player.dx += move_x * distance
            player.dy += move_y * distance

        # Check the bounds every frame, including rotation without movement.
        self.keep_player_inside_field()

    def keep_player_inside_field(self):
        player = self.model.player

        margin = player.get_bounding_radius() + player.line_width
        half_width = WIDTH / 2
        half_height = HEIGHT / 2

        player.dx = np.clip(
            player.dx,
            -half_width + margin,
            half_width - margin,
        )
        player.dy = np.clip(
            player.dy,
            -half_height + margin,
            half_height - margin,
        )


    def create_projectile(self):
        player = self.model.player
        angle_radians = np.deg2rad(player.angle)
        forward_x = np.cos(angle_radians)
        forward_y = np.sin(angle_radians)

        # Vertex 1 is the nose of our airplane geometry.
        nose_x, nose_y = player.get_world_vertices()[1, :2]
        projectile = WireframeObject(
            vertices=PROJECTILE_VERTICES,
            edges=PROJECTILE_EDGES,
            dx=nose_x + forward_x * 12.0,
            dy=nose_y + forward_y * 12.0,
            angle=player.angle,
            color=PROJECTILE_COLOR,
            line_width=2,
            velocity_x=forward_x * self.projectile_speed,
            velocity_y=forward_y * self.projectile_speed,
        )
        self.model.projectiles.append(projectile)

    def update_projectiles(self, delta_time):
        remaining = []
        margin = 40.0
        half_width = WIDTH / 2
        half_height = HEIGHT / 2

        for projectile in self.model.projectiles:
            projectile.dx += projectile.velocity_x * delta_time
            projectile.dy += projectile.velocity_y * delta_time

            # Keep the list being traversed intact; collect survivors separately.
            if (
                -half_width - margin <= projectile.dx <= half_width + margin
                and -half_height - margin <= projectile.dy <= half_height + margin
            ):
                remaining.append(projectile)

        self.model.projectiles = remaining


    def update_enemies(self, delta_time):
        for enemy in self.model.enemies:
            if enemy.motion_type == "diagonal":
                self.move_diagonal_enemy(enemy, delta_time)
            elif enemy.motion_type == "circle":
                self.move_circular_enemy(enemy, delta_time)

            # Visual spin has its own angle and angular speed.
            enemy.angle += enemy.angular_speed * delta_time
            enemy.angle %= 360

    def move_diagonal_enemy(self, enemy, delta_time):
        enemy.dx += enemy.velocity_x * delta_time
        enemy.dy += enemy.velocity_y * delta_time

        margin = enemy.get_bounding_radius() + enemy.line_width
        min_x = -WIDTH / 2 + margin
        max_x = WIDTH / 2 - margin
        min_y = -HEIGHT / 2 + margin
        max_y = HEIGHT / 2 - margin

        if enemy.dx < min_x:
            enemy.dx = min_x
            enemy.velocity_x *= -1
        elif enemy.dx > max_x:
            enemy.dx = max_x
            enemy.velocity_x *= -1

        if enemy.dy < min_y:
            enemy.dy = min_y
            enemy.velocity_y *= -1
        elif enemy.dy > max_y:
            enemy.dy = max_y
            enemy.velocity_y *= -1


    def move_circular_enemy(self, enemy, delta_time):
        enemy.orbit_angle += enemy.orbit_speed * delta_time
        enemy.orbit_angle %= 360
        angle_radians = np.deg2rad(enemy.orbit_angle)

        enemy.dx = enemy.orbit_center_x + enemy.orbit_radius * np.cos(angle_radians)
        enemy.dy = enemy.orbit_center_y + enemy.orbit_radius * np.sin(angle_radians)


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
        for game_object in self.model.get_all_objects():
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
