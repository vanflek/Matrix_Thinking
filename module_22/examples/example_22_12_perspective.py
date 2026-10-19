import numpy as np

WIDTH = 960
fov = np.deg2rad(60)
projection_distance = WIDTH / (2 * np.tan(fov / 2))

wall_height = 30.0
depths = np.array([75.0, 150.0, 300.0])
heights = wall_height * projection_distance / depths

print(f"d = {projection_distance:.2f}")
for i in range(depths.size):
    print(f"z = {depths[i]:.0f}, h = {heights[i]:.2f}")
