import numpy as np

brightness = np.array([80.0, 20.0, 50.0])
order = np.argsort(brightness, kind="stable")

print(order)
print(brightness)
print(brightness[order])
