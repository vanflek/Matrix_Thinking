import numpy as np
import pygame as pg

FONT_NAME = "consolas"
FONT_SIZE = 512


def measure_brightness(font, symbols):
    # Find one cell large enough for every symbol.
    cell_width = 0
    cell_height = 0

    for symbol in symbols:
        width, height = font.size(symbol)
        cell_width = max(cell_width, width)
        cell_height = max(cell_height, height)

    cell = pg.Surface((cell_width, cell_height), depth=32)
    brightness = np.zeros(len(symbols), dtype=float)

    for index, symbol in enumerate(symbols):
        # Remove the previous glyph before drawing the next one.
        cell.fill((255, 255, 255))
        symbol_image = font.render(
            symbol, True, (0, 0, 0), (255, 255, 255)
        )
        position = symbol_image.get_rect(
            center=cell.get_rect().center
        )
        cell.blit(symbol_image, position)
        pixels = pg.surfarray.array3d(cell)
        brightness[index] = pixels[:, :, 0].mean()

    return brightness


pg.font.init()
font_path = pg.font.match_font(FONT_NAME)
if font_path is None:
    pg.font.quit()
    raise FileNotFoundError("Install Consolas or choose another monospace font.")
font = pg.font.Font(font_path, FONT_SIZE)

symbols = []
for code in range(32, 127):
    symbols.append(chr(code))

brightness = measure_brightness(font, symbols)

for index, symbol in enumerate(symbols):
    print(ord(symbol), repr(symbol), brightness[index])
print("Measured symbols:", len(brightness))
pg.font.quit()
