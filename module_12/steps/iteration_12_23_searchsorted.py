import numpy as np
import pygame as pg

FONT_NAME = "consolas"
FONT_SIZE = 10
PALETTE_FILE = "symbol_palette.npz"


def get_gray(pixels):
    return (
        0.299 * pixels[:, :, 0]
        + 0.587 * pixels[:, :, 1]
        + 0.114 * pixels[:, :, 2]
    )


def get_cell_size(font):
    width = 0
    height = 0

    for code in range(32, 127):
        symbol_width, symbol_height = font.size(chr(code))
        width = max(width, symbol_width)
        height = max(height, symbol_height)

    return width, height


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


pg.init()
font_path = pg.font.match_font(FONT_NAME)
if font_path is None:
    pg.quit()
    raise FileNotFoundError("Install Consolas or choose the analyzer font.")
font = pg.font.Font(font_path, FONT_SIZE)
cell_width, cell_height = get_cell_size(font)

data = np.load(PALETTE_FILE)
symbols = data["symbols"]
brightness = data["brightness"]
data.close()
print("Palette shapes:", symbols.shape, brightness.shape)

image = pg.image.load("cat.png")
pixels = pg.surfarray.array3d(image)
gray = get_gray(pixels)
averages = get_block_averages(gray, cell_width, cell_height)
columns, rows = averages.shape
ascii_symbols = np.empty((columns, rows), dtype="<U1")
for x in range(columns):
    for y in range(rows):
        ascii_symbols[x, y] = block_to_ascii(averages[x, y], symbols, brightness)
print("ASCII array shape:", ascii_symbols.shape)
columns, rows = averages.shape
surface = pg.Surface(image.get_size())
surface.fill((255, 255, 255))
for x in range(columns):
    for y in range(rows):
        color = (0, 0, 0)
        symbol_image = font.render(
            ascii_symbols[x, y], True, color, (255, 255, 255)
        )
        cell_rect = pg.Rect(
            x * cell_width, y * cell_height, cell_width, cell_height
        )
        position = symbol_image.get_rect(center=cell_rect.center)
        surface.blit(symbol_image, position)

screen = pg.display.set_mode(surface.get_size())
pg.display.set_caption("ASCII learning step B10")
clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    if running:
        screen.blit(surface, (0, 0))
        pg.display.flip()
    clock.tick(60)
pg.quit()
