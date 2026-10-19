import numpy as np

side = np.array([15.0, 15.0, 15.0])
depth = np.array([60.0, 120.0, 240.0])
projection_distance = 800.0
camera_height = 15.0
scale = projection_distance / depth
screen_x = 800 / 2 + side * scale
screen_y = 480 // 2 + camera_height * scale

print(np.column_stack((screen_x, screen_y)))
