import time

import numpy as np
import pygame as pg

CELL_SIZE = 30
FPS = 60
MOUSE_SENSITIVITY = 0.003

GRID_COLOR = (112, 124, 137)
CEILING_COLOR = (45, 50, 65)
FLOOR_COLOR = (70, 60, 50)
BASE_WALL_COLOR = np.array([220, 180, 120], dtype=float)
SHADE_DISTANCE = 300.0


class GameModel:
    def __init__(self, maze):
        self.maze = maze
        self.rows, self.columns = maze.shape
        self.world_height = self.rows * CELL_SIZE
        self.world_width = self.columns * CELL_SIZE

        # This interior passage belongs to the supplied maze.npy.
        start_row, start_column = 8, 16
        assert maze[start_row, start_column] == 1

        # Store the observer's coordinates in the order [y, x].
        self.player_position = np.array([
            start_row + 0.5, start_column + 0.5
        ]) * CELL_SIZE
        self.player_angle = 0.0
        self.player_speed = 90.0
        self.floor_segments = self.create_floor_segments()


    def create_floor_segments(self):
        y = np.arange(self.rows + 1) * CELL_SIZE
        x = np.arange(self.columns + 1) * CELL_SIZE

        horizontal_start = np.column_stack((y, np.zeros_like(y)))
        horizontal_end = np.column_stack((
            y, np.zeros_like(y) + self.world_width
        ))
        horizontal = np.stack(
            (horizontal_start, horizontal_end), axis=1
        )

        vertical_start = np.column_stack((np.zeros_like(x), x))
        vertical_end = np.column_stack((
            np.zeros_like(x) + self.world_height, x
        ))
        vertical = np.stack((vertical_start, vertical_end), axis=1)
        return np.vstack((horizontal, vertical)).astype(float)


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
        actions["mouse_dx"] = pg.mouse.get_rel()[0]
        return actions


class GameLogic:
    def __init__(self, model):
        self.model = model
        self.actions = {}

    def apply_actions(self, actions):
        self.actions = actions

    def update(self, delta_time):
        # Mouse input is already a displacement, not a speed.
        self.model.player_angle += (
            self.actions["mouse_dx"] * MOUSE_SENSITIVITY
        )
        self.model.player_angle %= 2 * np.pi

        angle = self.model.player_angle
        # Both vectors use the coordinate order [y, x].
        forward = np.array([np.sin(angle), np.cos(angle)])
        right = np.array([np.cos(angle), -np.sin(angle)])

        movement = np.zeros(2, dtype=float)
        if self.actions["forward"]:
            movement += forward
        if self.actions["backward"]:
            movement -= forward
        if self.actions["right"]:
            movement += right
        if self.actions["left"]:
            movement -= right

        length = np.linalg.norm(movement)
        if length == 0:
            return

        direction = movement / length
        distance = self.model.player_speed * delta_time

        # Check short, axis-aligned moves to avoid skipping a wall.
        max_step = CELL_SIZE / 4
        step_count = int(distance / max_step) + 1
        step = direction * distance / step_count

        for _ in range(step_count):
            for axis in range(2):
                candidate = self.model.player_position.copy()
                candidate[axis] += step[axis]
                if self.can_move(candidate):
                    self.model.player_position = candidate

    def can_move(self, position):
        y, x = position
        # Validate world coordinates before indexing the matrix.
        if not (0 <= y < self.model.world_height
                and 0 <= x < self.model.world_width):
            return False

        row = int(y // CELL_SIZE)
        column = int(x // CELL_SIZE)
        return self.model.maze[row, column] == 1


class RayCaster:
    def __init__(self, model, screen_width):
        self.model = model
        self.fov = np.deg2rad(60)
        self.rays_count = 100
        self.ray_length = np.linalg.norm([
            model.world_height, model.world_width
        ])
        self.sample_count = int(self.ray_length * 16) + 2
        self.projection_distance = screen_width / (
            2 * np.tan(self.fov / 2)
        )
        stripe_width = screen_width / self.rays_count
        screen_x = (
            (np.arange(self.rays_count) + 0.5) * stripe_width
            - screen_width / 2
        )
        self.relative_angles = np.arctan(
            screen_x / self.projection_distance
        )
        self.distances = np.linspace(
            0, self.ray_length, self.sample_count
        )

    def ray_cast(self):
        ray_angles = self.model.player_angle + self.relative_angles
        sin_angles = np.sin(ray_angles)
        cos_angles = np.cos(ray_angles)
        player_y, player_x = self.model.player_position

        end_index = np.full(
            self.rays_count, self.sample_count - 1, dtype=int
        )
        has_wall = np.zeros(self.rays_count, dtype=bool)
        active_rays = np.arange(self.rays_count)
        batch_size = 256

        for start in range(0, self.sample_count, batch_size):
            distance_column = self.distances[
                start:start + batch_size, None
            ]
            ray_y = player_y + distance_column * sin_angles[active_rays]
            ray_x = player_x + distance_column * cos_angles[active_rays]
            cell_y = (ray_y // CELL_SIZE).astype(int)
            cell_x = (ray_x // CELL_SIZE).astype(int)
            inside = (
                (cell_y >= 0) & (cell_y < self.model.rows) &
                (cell_x >= 0) & (cell_x < self.model.columns)
            )
            walls = np.zeros_like(inside)
            walls[inside] = (
                self.model.maze[cell_y[inside], cell_x[inside]] == 0
            )
            batch_has_wall = walls.any(axis=0)
            first_hit = walls.argmax(axis=0)
            hit_rays = active_rays[batch_has_wall]
            end_index[hit_rays] = start + first_hit[batch_has_wall]
            has_wall[hit_rays] = True

            keep_searching = ~batch_has_wall & inside[-1]
            active_rays = active_rays[keep_searching]
            if active_rays.size == 0:
                break

        end_distance = self.distances[end_index]
        end_y = player_y + end_distance * sin_angles
        end_x = player_x + end_distance * cos_angles
        return end_y, end_x, end_distance, has_wall


    def ray_cast_full(self):
        ray_angles = self.model.player_angle + self.relative_angles
        sin_angles = np.sin(ray_angles)
        cos_angles = np.cos(ray_angles)
        distance_column = self.distances[:, None]

        player_y, player_x = self.model.player_position
        ray_y = player_y + distance_column * sin_angles
        ray_x = player_x + distance_column * cos_angles

        cell_y = (ray_y // CELL_SIZE).astype(int)
        cell_x = (ray_x // CELL_SIZE).astype(int)
        inside = (
            (cell_y >= 0) & (cell_y < self.model.rows) &
            (cell_x >= 0) & (cell_x < self.model.columns)
        )
        walls = np.zeros_like(inside)
        walls[inside] = (
            self.model.maze[cell_y[inside], cell_x[inside]] == 0
        )
        has_wall = walls.any(axis=0)
        first_hit = walls.argmax(axis=0)
        end_index = np.where(has_wall, first_hit, self.sample_count - 1)
        ray_indices = np.arange(self.rays_count)
        end_y = ray_y[end_index, ray_indices]
        end_x = ray_x[end_index, ray_indices]
        end_distance = self.distances[end_index]
        return end_y, end_x, end_distance, has_wall

    def ray_cast_batches(self):
        ray_angles = self.model.player_angle + self.relative_angles
        sin_angles = np.sin(ray_angles)
        cos_angles = np.cos(ray_angles)
        player_y, player_x = self.model.player_position

        end_index = np.full(
            self.rays_count, self.sample_count - 1, dtype=int
        )
        has_wall = np.zeros(self.rays_count, dtype=bool)
        batch_size = 256

        for start in range(0, self.sample_count, batch_size):
            distance_column = self.distances[
                start:start + batch_size, None
            ]
            ray_y = player_y + distance_column * sin_angles
            ray_x = player_x + distance_column * cos_angles
            cell_y = (ray_y // CELL_SIZE).astype(int)
            cell_x = (ray_x // CELL_SIZE).astype(int)
            inside = (
                (cell_y >= 0) & (cell_y < self.model.rows) &
                (cell_x >= 0) & (cell_x < self.model.columns)
            )
            walls = np.zeros_like(inside)
            walls[inside] = (
                self.model.maze[cell_y[inside], cell_x[inside]] == 0
            )
            batch_has_wall = walls.any(axis=0)
            new_hits = batch_has_wall & ~has_wall
            first_hit = walls.argmax(axis=0)
            end_index[new_hits] = start + first_hit[new_hits]
            has_wall[new_hits] = True

            if has_wall.all():
                break

        end_distance = self.distances[end_index]
        end_y = player_y + end_distance * sin_angles
        end_x = player_x + end_distance * cos_angles
        return end_y, end_x, end_distance, has_wall

    def get_camera_segments(self):
        relative = self.model.floor_segments - self.model.player_position
        dy = relative[:, :, 0]
        dx = relative[:, :, 1]
        angle = self.model.player_angle
        sin_angle = np.sin(angle)
        cos_angle = np.cos(angle)
        side = dy * cos_angle - dx * sin_angle
        depth = dy * sin_angle + dx * cos_angle
        return np.stack((side, depth), axis=2)

    def clip_floor_segments(self, camera_segments):
        near = 1.0
        visible = (camera_segments[:, :, 1] >= near).any(axis=1)
        clipped = camera_segments[visible].copy()
        start = clipped[:, 0].copy()
        end = clipped[:, 1].copy()
        start_inside = start[:, 1] >= near
        end_inside = end[:, 1] >= near
        crossing = start_inside != end_inside

        t = np.zeros(start.shape[0], dtype=float)
        np.divide(
            near - start[:, 1], end[:, 1] - start[:, 1],
            out=t, where=crossing,
        )
        intersection = start + t[:, None] * (end - start)
        intersection[:, 1] = near
        replace_start = crossing & ~start_inside
        replace_end = crossing & ~end_inside
        clipped[replace_start, 0] = intersection[replace_start]
        clipped[replace_end, 1] = intersection[replace_end]
        return clipped


    def project_floor_segments(self, clipped_segments, screen_width,
                               screen_height):
        side = clipped_segments[:, :, 0]
        depth = clipped_segments[:, :, 1]
        scale = self.projection_distance / depth
        camera_height = CELL_SIZE / 2
        screen_x = screen_width / 2 + side * scale
        screen_y = screen_height // 2 + camera_height * scale
        return np.stack((screen_x, screen_y), axis=2)

    def get_wall_heights(self, end_distance, has_wall):
        depths = end_distance * np.cos(self.relative_angles)
        wall_heights = np.zeros_like(end_distance, dtype=float)
        wall_heights[has_wall] = (
            CELL_SIZE * self.projection_distance
            / np.maximum(depths[has_wall], 1.0)
        )
        return wall_heights


class GameView:
    def __init__(self, screen):
        self.screen = screen


    def draw_first_person(self, wall_heights, end_distance, floor_segments):
        width, height = self.screen.get_size()
        horizon = height // 2
        self.screen.fill(CEILING_COLOR)
        pg.draw.rect(
            self.screen, FLOOR_COLOR,
            (0, horizon, width, height - horizon),
        )

        for segment in floor_segments:
            pg.draw.line(
                self.screen, GRID_COLOR,
                segment[0], segment[1], 1,
            )

        brightness = 1 / (1 + end_distance / SHADE_DISTANCE)
        wall_colors = (
            brightness[:, None] * BASE_WALL_COLOR
        ).astype(np.uint8)
        stripe_width = width / wall_heights.size

        for ray_index in range(wall_heights.size):
            wall_height = int(wall_heights[ray_index])
            if wall_height > 0:
                left = round(ray_index * stripe_width)
                right = round((ray_index + 1) * stripe_width)
                top = (height - wall_height) // 2
                pg.draw.rect(
                    self.screen, wall_colors[ray_index].tolist(),
                    (left, top, right - left, wall_height),
                )


class GameApp:
    def __init__(self, maze):
        pg.init()
        self.model = GameModel(maze)
        # Use the world dimensions as the window size.
        self.screen = pg.display.set_mode((
            self.model.world_width, self.model.world_height
        ))
        pg.display.set_caption("Raycasting: walls and floor grid")
        self.clock = pg.time.Clock()
        self.controller = InputController()
        self.logic = GameLogic(self.model)
        self.ray_caster = RayCaster(
            self.model, self.screen.get_width()
        )
        self.view = GameView(self.screen)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.mouse.get_rel()  # Discard motion accumulated during setup.

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
                result = self.ray_caster.ray_cast()
                end_y, end_x, end_distance, has_wall = result
                pg.display.set_caption(
                    f"Raycasting: {has_wall.sum()} / {has_wall.size} rays hit walls"
                )
                wall_heights = self.ray_caster.get_wall_heights(
                    end_distance, has_wall
                )
                camera_segments = self.ray_caster.get_camera_segments()
                clipped_segments = self.ray_caster.clip_floor_segments(
                    camera_segments
                )
                floor_segments = self.ray_caster.project_floor_segments(
                    clipped_segments, self.screen.get_width(),
                    self.screen.get_height()
                )
                self.view.draw_first_person(
                    wall_heights, end_distance, floor_segments
                )
                pg.display.flip()

        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        pg.quit()


def run_method(caster, mode):
    if mode == 0:
        return caster.ray_cast_full()
    if mode == 1:
        return caster.ray_cast_batches()
    return caster.ray_cast()


maze = np.load("maze.npy")
model = GameModel(maze)
caster = RayCaster(model, model.world_width)
start_position = model.player_position.copy()

# Select five passage centers distributed through the coordinate list.
free_cells = np.argwhere(maze == 1)
indices = np.linspace(0, len(free_cells) - 1, 5, dtype=int)
positions = (free_cells[indices] + 0.5) * CELL_SIZE
angles = [0.0, 0.4, 1.7, np.pi, 1.5 * np.pi, 6.1]
case_count = 0

for scenario in range(2):
    if scenario == 0:
        model.maze = maze
    else:
        model.maze = np.ones(maze.shape, dtype=np.uint8)

    for position in positions:
        model.player_position = position.copy()
        for angle in angles:
            model.player_angle = angle
            reference = caster.ray_cast_full()
            for mode in range(3):
                result = run_method(caster, mode)
                for index in range(4):
                    assert reference[index].shape == result[index].shape
                for index in range(3):
                    assert np.allclose(
                        reference[index], result[index],
                        rtol=0.0, atol=1e-9
                    )
                assert (reference[3] == result[3]).all()
                if scenario == 1:
                    assert not result[3].any()
                    assert (result[2] == caster.distances[-1]).all()
            case_count += 1
print(f"All {case_count} result comparisons passed.")

names = ["full", "batches", "active"]

for mode in range(3):
    # Restore the same scene before measuring each method.
    model.maze = maze
    model.player_position = start_position.copy()
    model.player_angle = 0.0
    run_method(caster, mode)
    times = []
    for repeat in range(5):
        start_time = time.perf_counter()
        result = run_method(caster, mode)
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        times.append(elapsed_ms)

    average_ms = sum(times) / len(times)
    print(f"{names[mode]}: answers match, {average_ms:.2f} ms")
