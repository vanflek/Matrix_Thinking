import numpy as np

symbols = np.array([" ", "#", "."], dtype="<U1")
brightness = np.array([235.0, 80.0, 255.0])

for index, symbol in enumerate(symbols):
    print(f"'{symbol}': {brightness[index]}")
