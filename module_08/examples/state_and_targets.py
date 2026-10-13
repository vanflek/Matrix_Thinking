import numpy as np


def move_player(state, shape):
    position = state["pos"]
    movement = state["vel"]

    state["pos"] = (position + movement) % np.array(shape)


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
print("Position vector:", state["pos"])
print("One component:", state["pos"][0])
move_player(state, (16, 16))
print("After one step:", state["pos"])

state["pos"] = np.array([5, 10], dtype=np.int16)
collect_target(state)
print("Remaining targets:")
print(state["targets"])
collect_target(state)
print("Visiting the same cell again:")
print(state["targets"])

# A repeated key replaces its earlier value; it adds no extra dictionary entry.
settings = {"speed": 5, "speed": 8}
print("Unique key:", settings)
