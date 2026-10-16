import numpy as np


def get_color_averages(pixels, cell_width, cell_height):
    columns = pixels.shape[0] // cell_width
    rows = pixels.shape[1] // cell_height

    cropped = pixels[
        :columns * cell_width,
        :rows * cell_height,
        :
    ]

    blocks = cropped.reshape(
        columns, cell_width,
        rows, cell_height,
        3
    )

    return blocks.mean(axis=(1, 3))


pixels = np.array([
    [[0, 0, 0], [200, 0, 0]],
    [[0, 100, 0], [0, 0, 100]]
], dtype=np.uint8)

colors = get_color_averages(pixels, 2, 2)

print(colors)
print(colors.shape)
