import numpy as np

symbols = np.array([".", "@", " "], dtype="<U1")
brightness = np.array([210.0, 90.0, 255.0])

order = np.argsort(brightness, kind="stable")

sorted_brightness = np.zeros_like(brightness)
sorted_symbols = np.empty_like(symbols)

for new_index, old_index in enumerate(order):
    sorted_brightness[new_index] = brightness[old_index]
    sorted_symbols[new_index] = symbols[old_index]

print(order)
print(sorted_symbols)
print(sorted_brightness)
