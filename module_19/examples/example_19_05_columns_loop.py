import numpy as np

radius = 10.0
angles_degrees = np.array([0.0, 30.0, 60.0, 90.0])

angles_radians = np.deg2rad(angles_degrees)

x_values = radius * np.cos(angles_radians)
y_values = radius * np.sin(angles_radians)

points = []

for i in range(len(x_values)):
    points.append([x_values[i], y_values[i]])

points = np.array(points)

print("Points:")
print(points)
print("Shape:", points.shape)
