import numpy as np

radius = 10.0
angle_degrees = 60.0

angle_radians = np.deg2rad(angle_degrees)

cos_value = np.cos(angle_radians)
sin_value = np.sin(angle_radians)

x = radius * cos_value
y = radius * sin_value

print("Angle in degrees:", angle_degrees)
print("Angle in radians:", angle_radians)
print("Cosine:", cos_value)
print("Sine:", sin_value)
print("Coordinates:", x, y)
