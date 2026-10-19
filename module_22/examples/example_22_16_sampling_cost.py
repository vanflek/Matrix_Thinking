import numpy as np

ray_length = np.linalg.norm([480, 960])
for rays_count, density in [(60, 1), (100, 1), (100, 16)]:
    if density == 1:
        sample_count = int(ray_length) + 1
    else:
        sample_count = int(ray_length * density) + 2
    point_count = sample_count * rays_count
    matrix_bytes = point_count * 8
    print(rays_count, sample_count, point_count, matrix_bytes)
