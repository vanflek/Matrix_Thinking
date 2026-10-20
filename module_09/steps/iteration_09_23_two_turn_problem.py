# Reproduce two turns before a movement step
import numpy as np


def change_direction(state, new_direction):
    if not np.array_equal(new_direction, -state["vel"]):
        state["vel"] = new_direction


state = {
    "vel": np.array([0, 1], dtype=np.int16),
}

change_direction(
    state,
    np.array([0, -1], dtype=np.int16),
)
print("After Left:", state["vel"])

change_direction(
    state,
    np.array([-1, 0], dtype=np.int16),
)
print("After Up:", state["vel"])

change_direction(
    state,
    np.array([1, 0], dtype=np.int16),
)
print("After Down:", state["vel"])

state["vel"] = np.array([0, 1], dtype=np.int16)

change_direction(
    state,
    np.array([-1, 0], dtype=np.int16),
)
change_direction(
    state,
    np.array([0, -1], dtype=np.int16),
)

print("After two turns:", state["vel"])
