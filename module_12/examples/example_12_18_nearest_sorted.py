import numpy as np


def block_to_ascii(block, symbols, brightness):
    right = np.searchsorted(
        brightness, block, side="right"
    )

    if right == 0:
        return symbols[0]

    if right == len(brightness):
        return symbols[-1]

    left = right - 1

    left_distance = block - brightness[left]
    right_distance = brightness[right] - block

    if left_distance <= right_distance:
        return symbols[left]

    return symbols[right]


symbols = np.array(["@", "#", ".", " "], dtype="<U1")
brightness = np.array([0.0, 30.0, 70.0, 255.0])

print(block_to_ascii(65.0, symbols, brightness))
print(block_to_ascii(50.0, symbols, brightness))
print(block_to_ascii(-5.0, symbols, brightness))
