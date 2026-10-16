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


def blocks_to_ascii(averages, symbols, brightness):
    right = np.searchsorted(
        brightness, averages, side="right"
    )
    left = right - 1

    last = len(brightness) - 1
    left = np.clip(left, 0, last)
    right = np.clip(right, 0, last)

    left_distance = np.abs(
        averages - brightness[left]
    )
    right_distance = np.abs(
        averages - brightness[right]
    )

    choose_left = left_distance <= right_distance
    indices = np.where(choose_left, left, right)

    return symbols[indices]


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
colors = get_color_averages(pixels, cell_width, cell_height)
draw_colors = colors.astype(np.uint8)
ascii_symbols = blocks_to_ascii(averages, symbols, brightness)
columns, rows = averages.shape
surface = pg.Surface(image.get_size())
surface.fill((255, 255, 255))
for x in range(columns):
    for y in range(rows):
        color = tuple(draw_colors[x, y])
        symbol_image = font.render(
            ascii_symbols[x, y], True, color, (255, 255, 255)
        )
        cell_rect = pg.Rect(
            x * cell_width, y * cell_height, cell_width, cell_height
        )
        position = symbol_image.get_rect(center=cell_rect.center)
        surface.blit(symbol_image, position)

screen = pg.display.set_mode(surface.get_size())
pg.display.set_caption("ASCII learning step B14")
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
