# Count the cells in preceding rows, using the number of columns per row.
ROWS = 5
COLS = 8
addresses = [(0, 7), (1, 0), (1, 2), (4, 7)]

for row, col in addresses:
    index = row * COLS + col
    print(row, col, index)
