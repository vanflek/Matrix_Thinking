import pygame as pg

FONT_NAME = "consolas"
FONT_SIZE = 512

# Initialize only the font module: no window is needed.
pg.font.init()

font_path = pg.font.match_font(FONT_NAME)

if font_path is None:
    pg.font.quit()
    raise FileNotFoundError(
        "Install Consolas or choose another monospace font."
    )

font = pg.font.Font(font_path, FONT_SIZE)

symbol = chr(64)
width, height = font.size(symbol)

# Prepare a white cell for the selected symbol.
cell = pg.Surface((width, height), depth=32)
cell.fill((255, 255, 255))

symbol_image = font.render(
    symbol, True, (0, 0, 0), (255, 255, 255)
)

position = symbol_image.get_rect(
    center=cell.get_rect().center
)
cell.blit(symbol_image, position)

# Copy the pixels into an independent NumPy array.
pixels = pg.surfarray.array3d(cell)

print("Symbol:", symbol, "Code:", ord(symbol))
print("Pixel array shape (X, Y, RGB):", pixels.shape)

pg.image.save(cell, "symbol_sample.png")
print("Saved symbol_sample.png without opening a window.")

total = 0
for x in range(width):
    for y in range(height):
        total += int(pixels[x, y, 0])
brightness = total / (width * height)
print("Mean brightness:", brightness)

pg.font.quit()
