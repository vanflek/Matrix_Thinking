import numpy as np

player_position = np.array([45.0, 45.0])
player_y, player_x = player_position

ray_angles = np.array([-30, 0, 30])
ray_distances = np.array([0, 10, 20, 30])

angle_grid, distance_grid = np.meshgrid(
    ray_angles, ray_distances
)
angles_radians = np.deg2rad(angle_grid)

ray_y = player_y + distance_grid * np.sin(angles_radians)
ray_x = player_x + distance_grid * np.cos(angles_radians)

print(ray_y)
print(ray_x)
print(ray_y.shape)
print(ray_x.shape)
print(ray_y[2, 1], ray_x[2, 1])
