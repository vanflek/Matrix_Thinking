import numpy as np

screen_width = 800
rays_count = 4
fov = np.deg2rad(60)
projection_distance = screen_width / (2 * np.tan(fov / 2))
stripe_width = screen_width / rays_count
centers = (np.arange(rays_count) + 0.5) * stripe_width
screen_x = centers - screen_width / 2
relative_angles = np.arctan(screen_x / projection_distance)

print(centers)
print(screen_x)
print(np.round(np.rad2deg(relative_angles), 2))
