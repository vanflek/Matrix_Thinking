import numpy as np


# World-to-camera rotation for yaw = 90 degrees, pitch = roll = 0.
rotation = np.array([
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 0, 1],
], dtype=float)

movement_camera = np.array([0, 0, 1, 0], dtype=float)
movement_world = movement_camera @ rotation.T

print(movement_world)
print(movement_world @ rotation)
