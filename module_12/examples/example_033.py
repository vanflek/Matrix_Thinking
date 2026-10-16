import numpy as np


def normalize_brightness(brightness):
    minimum = brightness.min()
    maximum = brightness.max()

    if maximum == minimum:
        return np.zeros_like(brightness)

    return (
        (brightness - minimum)
        / (maximum - minimum)
        * 255
    )


values = np.array([180.0, 210.0, 240.0])
print(normalize_brightness(values))

same_values = np.array([210.0, 210.0, 210.0])
print(normalize_brightness(same_values))
