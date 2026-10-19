import numpy as np

distances = np.array([0.0, 10.0, 20.0])
angles = np.deg2rad([-30.0, 0.0, 30.0])
distance_column = distances[:, None]
sin_angles = np.sin(angles)
cos_angles = np.cos(angles)
ray_y = 100 + distance_column * sin_angles
ray_x = 200 + distance_column * cos_angles

print(distance_column.shape)
print(sin_angles.shape)
print(np.round(ray_y, 2))
print(np.round(ray_x, 2))
