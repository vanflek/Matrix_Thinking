import numpy as np


def get_block_averages(gray, cell_width, cell_height):
    columns = gray.shape[0] // cell_width
    rows = gray.shape[1] // cell_height

    cropped = gray[
        :columns * cell_width,
        :rows * cell_height
    ]

    blocks = cropped.reshape(
        columns, cell_width,
        rows, cell_height
    )

    return blocks.mean(axis=(1, 3))


gray = np.arange(24).reshape(6, 4)

averages = get_block_averages(gray, 2, 2)
print(averages)
