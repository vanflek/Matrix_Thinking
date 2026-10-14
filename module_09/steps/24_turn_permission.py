# Allow one turn per completed step
import numpy as np


def change_direction(state, new_direction):
    if not state["can_turn"]:
        return

    if np.array_equal(new_direction, state["vel"]):
        return

    if np.array_equal(new_direction, -state["vel"]):
        return

    state["vel"] = new_direction
    state["can_turn"] = False


state = {
    "vel": np.array([0, 1], dtype=np.int16),
    "can_turn": True,
}

change_direction(
    state,
    np.array([-1, 0], dtype=np.int16),
)
print("After Up:", state["vel"])
print("Can turn:", state["can_turn"])

change_direction(
    state,
    np.array([0, -1], dtype=np.int16),
)
print("After Left:", state["vel"])

# Simulate restoring permission after a completed step.
state["can_turn"] = True

change_direction(
    state,
    np.array([0, -1], dtype=np.int16),
)
print("After step and Left:", state["vel"])
