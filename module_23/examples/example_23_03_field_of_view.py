import numpy as np


WIDTH = 1000

for angle_degrees in (30, 60, 90):
    fov = np.deg2rad(angle_degrees)
    distance = WIDTH / (2 * np.tan(fov / 2))
    print(f"FOV={angle_degrees}: d={distance:.2f}")
