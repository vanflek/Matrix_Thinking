import numpy as np

# A vector with components 3 and 4 has length 5.
move_x = 3.0
move_y = 4.0
length = np.hypot(move_x, move_y)
print(length)

# Divide a nonzero vector by its length to preserve direction.
move_x /= length
move_y /= length
print(move_x, move_y)
print(np.hypot(move_x, move_y))
