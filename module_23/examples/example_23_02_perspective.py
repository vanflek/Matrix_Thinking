import numpy as np


WIDTH, HEIGHT = 1000, 1000
PROJECTIVE_DISTANCE = 500.0

camera_vertices = np.array([
    [2, 1, 5, 1],
    [2, 1, 10, 1],
], dtype=float)

projective_matrix = np.array([
    [PROJECTIVE_DISTANCE, 0, 0, 0],
    [0, PROJECTIVE_DISTANCE, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 0],
])

projected = camera_vertices @ projective_matrix
w = projected[:, 3]
offset_x = projected[:, 0] / w
offset_y = projected[:, 1] / w

screen_x = WIDTH / 2 + offset_x
screen_y = HEIGHT / 2 - offset_y
screen_vertices = np.column_stack((screen_x, screen_y))

print(screen_vertices)
