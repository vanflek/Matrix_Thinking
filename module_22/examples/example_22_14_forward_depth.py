import numpy as np

relative_angles = np.deg2rad([-30.0, 0.0, 30.0])
ray_lengths = np.array([200 / np.cos(np.deg2rad(30)), 200.0,
                        200 / np.cos(np.deg2rad(30))])
depths = ray_lengths * np.cos(relative_angles)

print(np.round(ray_lengths, 2))
print(np.round(depths, 2))
print(np.round(30 * 800 / ray_lengths, 2))
print(np.round(30 * 800 / depths, 2))
