# A local assignment leaves an outside name unchanged.
def calculate_pixel_size(cell_count, cell_size):
    pixel_size = cell_count * cell_size
    return pixel_size

pixel_size = 100
width = calculate_pixel_size(16, 40)
print(pixel_size)
print(width)
