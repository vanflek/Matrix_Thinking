# Only visiting a target removes its coordinate row.
import numpy as np

def collect_target(state):
    position = state["pos"]

    for index, target in enumerate(state["targets"]):
        if position[0] == target[0] and position[1] == target[1]:
            state["targets"] = np.delete(
                state["targets"], index, axis=0
            )
            return

state = {
    "pos": np.array([8, 8], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([[2, 3], [5, 10], [12, 6]], dtype=np.int16),
}

state["pos"] = np.array([0, 0], dtype=np.int16)
collect_target(state)
print(len(state["targets"]))
state["pos"] = np.array([5, 10], dtype=np.int16)
collect_target(state)
print(state["targets"])
print(len(state["targets"]))
collect_target(state)
print(len(state["targets"]))
