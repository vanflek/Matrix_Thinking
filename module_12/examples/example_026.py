import numpy as np


def normalize_brightness(brightness):
    minimum = brightness[0]
    maximum = brightness[0]

    for value in brightness:
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value

    normalized = np.zeros(len(brightness), dtype=float)

    if maximum == minimum:
        return normalized

    for index in range(len(brightness)):
        normalized[index] = (
            (brightness[index] - minimum)
            / (maximum - minimum)
            * 255
        )

    return normalized


values = np.array([180.0, 210.0, 240.0])
print(normalize_brightness(values))

same_values = np.array([210.0, 210.0, 210.0])
print(normalize_brightness(same_values))
