import numpy as np

has_wall = np.array([True, True, True, False])
first_hit = np.array([2, 1, 3, 0])
sample_count = 5
rays_count = 4

end_index = np.where(has_wall, first_hit, sample_count - 1)
ray_indices = np.arange(rays_count)

values = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
    [40, 41, 42, 43],
    [50, 51, 52, 53],
])
selected = values[end_index, ray_indices]

distances = np.linspace(0, 40, sample_count)
end_distance = distances[end_index]

print(end_index)
print(ray_indices)
print(selected)
print(end_distance)
