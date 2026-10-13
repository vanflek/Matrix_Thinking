# Dictionary keys provide access to whole arrays.
import numpy as np

state = {
    "pos": np.array([8, 8], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([[2, 3], [5, 10], [12, 6]], dtype=np.int16),
}

print(state["pos"])
print(state["vel"])
print(state["targets"])
print(len(state["targets"]))
