import numpy as np

brightness = np.array([0.0, 30.0, 70.0, 255.0])

right = np.searchsorted(
    brightness, 65.0, side="right"
)

print(right)
