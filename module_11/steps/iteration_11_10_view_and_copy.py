import numpy as np

matrix = np.array([[[20, 40, 60]]], dtype=np.uint8)

view_color = matrix[0, 0]
copied_color = matrix[0, 0].copy()

brush_rgb = np.zeros(3, dtype=np.uint8)
brush_rgb[:] = matrix[0, 0]

view_color[0] = 200

print("After changing the view:")
print("Cell:", matrix[0, 0])
print("View:", view_color)
print("Copy:", copied_color)
print("Brush:", brush_rgb)

copied_color[1] = 150
brush_rgb[2] = 180

print("After changing the copy and the brush:")
print("Cell:", matrix[0, 0])
print("View:", view_color)
print("Copy:", copied_color)
print("Brush:", brush_rgb)

matrix[0, 0, 1] = 90

print(view_color)
print(copied_color)
print(brush_rgb)
