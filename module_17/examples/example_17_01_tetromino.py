import numpy as np


TETROMINOES = {
    "I": np.array([
        [1, 1, 1, 1],
    ], dtype=np.uint8),

    "O": np.array([
        [2, 2],
        [2, 2],
    ], dtype=np.uint8),

    "T": np.array([
        [0, 3, 0],
        [3, 3, 3],
    ], dtype=np.uint8),

    "L": np.array([
        [4, 0],
        [4, 0],
        [4, 4],
    ], dtype=np.uint8),

    "J": np.array([
        [0, 5],
        [0, 5],
        [5, 5],
    ], dtype=np.uint8),

    "S": np.array([
        [0, 6, 6],
        [6, 6, 0],
    ], dtype=np.uint8),

    "Z": np.array([
        [7, 7, 0],
        [0, 7, 7],
    ], dtype=np.uint8),
}


class Tetromino:
    def __init__(self, matrix, x=0, y=0, rotation=0):
        self.matrix = matrix.copy()
        self.x = x
        self.y = y
        self.rotation = rotation

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_matrix(self):
        return np.rot90(self.matrix, self.rotation)


piece = Tetromino(TETROMINOES["T"], x=3, y=2)

print("Position:", piece.x, piece.y)
print("Rotation:", piece.rotation)
print(piece.get_matrix())

piece.move(1, 2)
piece.rotate()

print("Position:", piece.x, piece.y)
print("Rotation:", piece.rotation)
print(piece.get_matrix())
