import numpy as np

symbols = np.array([".", "@", " "], dtype="<U1")
brightness = np.array([210.0, 90.0, 255.0])

order = np.argsort(brightness, kind="stable")
brightness = brightness[order]

print(symbols[0], brightness[0])
