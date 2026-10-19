import time

import numpy as np


def get_depths_loop(distances, angles):
    depths = np.zeros(distances.shape, dtype=float)
    for index in range(distances.size):
        depths[index] = distances[index] * np.cos(angles[index])
    return depths


def get_depths_numpy(distances, angles):
    return distances * np.cos(angles)


distances = np.array([200.0, 200.0, 200.0])
angles = np.deg2rad(np.array([-30.0, 0.0, 30.0]))
reference = get_depths_loop(distances, angles)
result = get_depths_numpy(distances, angles)

# Check the structure before comparing numerical values.
assert reference.shape == result.shape
assert np.allclose(reference, result, rtol=0.0, atol=1e-9)
print("Answers match:", np.round(result, 2))

# Warm up before measuring. Use the same inputs for both functions.
get_depths_loop(distances, angles)
get_depths_numpy(distances, angles)

start_time = time.perf_counter()
reference = get_depths_loop(distances, angles)
loop_ms = (time.perf_counter() - start_time) * 1000

start_time = time.perf_counter()
result = get_depths_numpy(distances, angles)
numpy_ms = (time.perf_counter() - start_time) * 1000

print(f"Loop: {loop_ms:.6f} ms")
print(f"NumPy: {numpy_ms:.6f} ms")
