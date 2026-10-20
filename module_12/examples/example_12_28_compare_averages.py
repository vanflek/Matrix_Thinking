import numpy as np


def averages_four_loops(gray, cell_width, cell_height):
    columns = gray.shape[0] // cell_width
    rows = gray.shape[1] // cell_height
    averages = np.zeros((columns, rows), dtype=float)

    for x in range(columns):
        for y in range(rows):
            left = x * cell_width
            top = y * cell_height

            block = gray[
                left:left + cell_width,
                top:top + cell_height
            ]

            total = 0.0
            for local_x in range(cell_width):
                for local_y in range(cell_height):
                    total += block[local_x, local_y]

            averages[x, y] = total / (cell_width * cell_height)

    return averages


def averages_block_mean(gray, cell_width, cell_height):
    columns = gray.shape[0] // cell_width
    rows = gray.shape[1] // cell_height
    averages = np.zeros((columns, rows), dtype=float)

    for x in range(columns):
        for y in range(rows):
            left = x * cell_width
            top = y * cell_height

            block = gray[
                left:left + cell_width,
                top:top + cell_height
            ]

            averages[x, y] = block.mean()

    return averages


def averages_numpy(gray, cell_width, cell_height):
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


gray = np.arange(14 * 11, dtype=float).reshape(14, 11)

print(averages_four_loops(gray, 4, 3))
print(averages_block_mean(gray, 4, 3))
print(averages_numpy(gray, 4, 3))
