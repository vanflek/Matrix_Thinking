import numpy as np

base_color = np.array([220, 180, 120], dtype=float)
distances = np.array([0.0, 150.0, 300.0, 600.0])

brightness = 1 / (1 + distances / 300.0)
brightness_column = brightness[:, None]
wall_colors = (brightness_column * base_color).astype(np.uint8)

print(brightness)
print(brightness.shape)
print(brightness_column.shape)
print(wall_colors)
print(wall_colors.shape)
