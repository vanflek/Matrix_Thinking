import numpy as np

player_position = np.array([45.0, 45.0])
player_y, player_x = player_position
angle = 0.0

ray_length = 40.0
sample_count = 5
distances = np.linspace(0, ray_length, sample_count)

ray_y = player_y + distances * np.sin(angle)
ray_x = player_x + distances * np.cos(angle)
points = np.column_stack((ray_y, ray_x))

print(distances)
print(points)
