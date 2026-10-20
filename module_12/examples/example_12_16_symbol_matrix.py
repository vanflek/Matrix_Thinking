import numpy as np


def block_to_ascii(block, symbols, brightness):
    best_index = 0
    best_distance = abs(block - brightness[0])

    for index in range(1, len(brightness)):
        distance = abs(block - brightness[index])

        if distance < best_distance:
            best_distance = distance
            best_index = index

    return symbols[best_index]


symbols = np.array(["@", "#", ".", " "], dtype="<U1")
brightness = np.array([0.0, 30.0, 70.0, 255.0])

averages = np.array([
    [5.0, 65.0],
    [180.0, 255.0]
])

ascii_symbols = np.empty(averages.shape, dtype="<U1")

for x in range(averages.shape[0]):
    for y in range(averages.shape[1]):
        ascii_symbols[x, y] = block_to_ascii(
            averages[x, y],
            symbols,
            brightness
        )

print(ascii_symbols)
