import numpy as np

radius = 10.0
angles_degrees = np.array([0.0, 30.0, 60.0, 90.0])

x_values = []
y_values = []

for angle_degrees in angles_degrees:
    angle_radians = np.deg2rad(angle_degrees)

    x = radius * np.cos(angle_radians)
    y = radius * np.sin(angle_radians)

    x_values.append(x)
    y_values.append(y)

x_values = np.array(x_values)
y_values = np.array(y_values)

print("Angles:", angles_degrees)
print("X:", x_values)
print("Y:", y_values)
