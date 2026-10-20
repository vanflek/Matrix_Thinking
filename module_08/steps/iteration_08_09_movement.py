# Check an ordinary step and wrapping on two axes.
import numpy as np

def move_player(state, shape):
    position = state["pos"]
    movement = state["vel"]

    state["pos"] = (position + movement) % np.array(shape)

state = {
    "pos": np.array([8, 8], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([[2, 3], [5, 10], [12, 6]], dtype=np.int16),
}

move_player(state, (16, 16))
print(state["pos"])
state["pos"] = np.array([8, 15], dtype=np.int16)
move_player(state, (16, 16))
print(state["pos"])
state["pos"] = np.array([0, 8], dtype=np.int16)
state["vel"] = np.array([-1, 0], dtype=np.int16)
move_player(state, (16, 16))
print(state["pos"])
