import numpy as np

brightness = np.array([0.0, 30.0, 70.0, 255.0])

averages = np.array([
    [5.0, 65.0],
    [180.0, 255.0]
])

right = np.searchsorted(
    brightness, averages, side="right"
)
left = right - 1

print(right)
print(left)
