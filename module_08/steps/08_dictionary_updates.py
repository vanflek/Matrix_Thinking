# Changing data and replacing a dictionary entry.
import numpy as np

state = {
    "pos": np.array([8, 8], dtype=np.int16),
    "vel": np.array([0, 1], dtype=np.int16),
    "targets": np.array([[2, 3], [5, 10], [12, 6]], dtype=np.int16),
}

state["pos"][0] = 4
print(state["pos"])
state["pos"] = np.array([1, 2], dtype=np.int16)
print(state["pos"])
settings = {"cell_size": 20, "cell_size": 40}
print(settings["cell_size"])
print(len(settings))
