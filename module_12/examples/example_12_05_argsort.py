import numpy as np

brightness = np.array([210.0, 90.0, 255.0])
order = np.argsort(brightness, kind="stable")

print(order)
