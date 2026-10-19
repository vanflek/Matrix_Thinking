import numpy as np

camera = np.array([100.0, 200.0])
points = np.array([[100.0, 230.0], [120.0, 200.0], [100.0, 180.0]])
relative = points - camera
dy = relative[:, 0]
dx = relative[:, 1]

for angle in [0.0, np.pi / 2]:
    side = dy * np.cos(angle) - dx * np.sin(angle)
    depth = dy * np.sin(angle) + dx * np.cos(angle)
    print(np.round(np.column_stack((side, depth)), 2))
