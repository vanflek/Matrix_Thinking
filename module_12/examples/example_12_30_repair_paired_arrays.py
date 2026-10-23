import numpy as np

symbols = np.array([" ", "#", "."], dtype="<U1")

# Restore the measured brightness for each symbol in its current position.
brightness = np.array([255.0, 80.0, 235.0])

for index, symbol in enumerate(symbols):
    print(f"'{symbol}': {brightness[index]}")
