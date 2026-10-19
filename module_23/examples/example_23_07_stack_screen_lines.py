import numpy as np


screen_x = np.array([[100, 200], [300, 400]])
screen_y = np.array([[10, 20], [30, 40]])

screen_lines = np.stack((screen_x, screen_y), axis=2)

print(screen_lines)
print(screen_lines.shape)
