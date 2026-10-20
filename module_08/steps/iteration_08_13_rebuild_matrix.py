# Rebuilding clears the previous player position.
import numpy as np

TARGET_COLOR_INDEX = 3
PLAYER_COLOR_INDEX = 5

def move_player(state, shape):
    position = state["pos"]
    movement = state["vel"]

    state["pos"] = (position + movement) % np.array(shape)

def rebuild_matrix(matrix, state):
    matrix.fill(0)

    for row, col in state["targets"]:
        matrix[row, col] = TARGET_COLOR_INDEX

    row, col = state["pos"]
    matrix[row, col] = PLAYER_COLOR_INDEX

state = {
    "pos": np.array([1, 1], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([[0, 3], [2, 0]], dtype=np.int16),
}
matrix = np.zeros((3, 4), dtype=np.uint8)
rebuild_matrix(matrix, state)
print(matrix)
move_player(state, matrix.shape)
rebuild_matrix(matrix, state)
print(matrix)
