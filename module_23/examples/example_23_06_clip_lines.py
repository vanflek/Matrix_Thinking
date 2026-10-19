import numpy as np


class GameLogic:
    def clip_lines(self, lines, near):
        depths = lines[:, :, 2]
        keep = (depths >= near).any(axis=1)
        lines = lines[keep]

        for end in range(2):
            other = 1 - end
            behind = lines[:, end, 2] < near
            start_points = lines[behind, end]
            end_points = lines[behind, other]
            t = (
                (near - start_points[:, 2])
                / (end_points[:, 2] - start_points[:, 2])
            )
            lines[behind, end] = (
                start_points + t[:, None] * (end_points - start_points)
            )
            lines[behind, end, 2] = near

        return lines


vertices = np.array([
    [-2, 1, -1, 1],
    [4, 3, 5, 1],
    [2, -1, 3, 1],
    [0, 0, -2, 1],
    [1, 1, -3, 1],
    [0, 0, 2, 1],
    [1, 0, 4, 1],
], dtype=float)

edges = np.array([
    [0, 1],
    [0, 2],
    [3, 4],
    [5, 6],
], dtype=np.intp)

near = 1.0
lines = vertices[edges]
clipped = GameLogic().clip_lines(lines, near)

print(lines.shape)
print((lines[:, :, 2] >= near).any(axis=1))
print(clipped.shape)
print(clipped[:, 0, :3])
print(vertices[0])
