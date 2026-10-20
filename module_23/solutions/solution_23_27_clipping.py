import numpy as np
from wireframe_scene import GameLogic

logic = GameLogic()
near = 1.0
lines = np.array([
    [[0, 0, 2, 1], [1, 0, 5, 1]],
    [[0, 0, -2, 1], [1, 0, 0.5, 1]],
    [[-4, 2, -2, 1], [2, -1, 4, 1]],
    [[0, 0, 1, 1], [1, 0, 4, 1]],
], dtype=float)
original = lines.copy()
result = logic.clip_lines(lines, near)
assert result.shape == (3, 2, 4)
assert np.allclose(result[0], lines[0])
assert np.allclose(result[2], lines[3])
assert np.all(result[:, :, 2] >= near)
assert np.array_equal(lines, original)
assert np.allclose(result[1, 0], [-1, 0.5, 1, 1])
empty = logic.clip_lines(lines[1:2], near)
assert empty.shape == (0, 2, 4)
reverse = logic.clip_lines(lines[2:3, ::-1], near)
assert np.allclose(reverse, result[1:2, ::-1])
print("All clipping checks passed")
