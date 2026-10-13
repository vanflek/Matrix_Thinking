# Use a returned value outside the function.
def calculate_pixel_size(cell_count, cell_size):
    pixel_size = cell_count * cell_size
    return pixel_size

width = calculate_pixel_size(16, 40)
height = calculate_pixel_size(12, 40)
print(width, height)
