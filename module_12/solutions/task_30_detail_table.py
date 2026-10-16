import numpy as np
import pygame as pg

def get_cell_size(font):
    width = 0
    height = 0

    for code in range(32, 127):
        symbol_width, symbol_height = font.size(chr(code))
        width = max(width, symbol_width)
        height = max(height, symbol_height)

    return width, height

pg.font.init()
font_path = pg.font.match_font("consolas")
if font_path is None:
    pg.font.quit()
    raise FileNotFoundError("Install Consolas or choose the analyzer font.")
image = pg.image.load("cat.png")
width, height = image.get_size()
print("Font size | Cell width | Cell height | Columns | Rows")
for size in (8, 16, 32):
    font = pg.font.Font(font_path, size)
    cell_width, cell_height = get_cell_size(font)
    print(size, cell_width, cell_height, width // cell_width, height // cell_height)
pg.font.quit()
