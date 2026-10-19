import numpy as np

# Use degrees here to make the printed matrices easy to read.
ray_angles = np.array([-30, 0, 30])
ray_distances = np.array([0, 10, 20, 30])

angle_grid, distance_grid = np.meshgrid(
    ray_angles, ray_distances
)

print(angle_grid)
print(distance_grid)
print(angle_grid.shape)
print(distance_grid.shape)
print(angle_grid[2, 1], distance_grid[2, 1])
