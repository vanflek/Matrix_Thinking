import numpy as np

WIDTH, HEIGHT = 800, 600
points = np.array([
    [2.0, 1.0, 4.0, 1.0],
    [2.0, 1.0, 8.0, 1.0],
    [4.0, 2.0, 8.0, 1.0],
])

for degrees in (90, 60):
    fov = np.deg2rad(degrees)
    d = WIDTH / (2 * np.tan(fov / 2))
    formula = np.column_stack((
        WIDTH / 2 + d * points[:, 0] / points[:, 2],
        HEIGHT / 2 - d * points[:, 1] / points[:, 2],
    ))
    matrix = np.array([
        [d, 0, 0, 0],
        [0, d, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0],
    ])
    projected = points @ matrix
    screen = np.column_stack((
        WIDTH / 2 + projected[:, 0] / projected[:, 3],
        HEIGHT / 2 - projected[:, 1] / projected[:, 3],
    ))
    assert np.allclose(formula, screen)
    assert np.allclose(screen[0], screen[2])
    print(degrees)
    print(np.round(screen, 2))
