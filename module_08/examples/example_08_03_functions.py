# Parameters receive arguments; return passes a result to the caller.
def show_rules(target_count):
    print(f"Collect {target_count} targets.")
    print("Use the arrow keys to change direction.")
    print("Visit every target to win.")


def calculate_pixel_size(cell_count, cell_size):
    pixel_size = cell_count * cell_size
    return pixel_size


show_rules(3)
show_rules(5)
number_of_targets = 7
show_rules(number_of_targets)

COLS = 16
ROWS = 12
CELL_SIZE = 40
width = calculate_pixel_size(COLS, CELL_SIZE)
height = calculate_pixel_size(ROWS, CELL_SIZE)
print("Window size:", width, height)

# The local variable inside the function does not overwrite this one.
pixel_size = 100
width = calculate_pixel_size(6, 20)
print("Outside pixel_size:", pixel_size)
print("Returned width:", width)
