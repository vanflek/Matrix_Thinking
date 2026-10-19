import numpy as np


def clip_loop(camera_segments, near):
    visible = (camera_segments[:, :, 1] >= near).any(axis=1)
    clipped = camera_segments[visible].copy()

    for segment in clipped:
        start = segment[0].copy()
        end = segment[1].copy()
        start_inside = start[1] >= near
        end_inside = end[1] >= near
        if start_inside != end_inside:
            t = (near - start[1]) / (end[1] - start[1])
            intersection = start + t * (end - start)
            intersection[1] = near
            if not start_inside:
                segment[0] = intersection
            else:
                segment[1] = intersection
    return clipped


def clip_numpy(camera_segments, near):
    visible = (camera_segments[:, :, 1] >= near).any(axis=1)
    clipped = camera_segments[visible].copy()
    start = clipped[:, 0].copy()
    end = clipped[:, 1].copy()
    start_inside = start[:, 1] >= near
    end_inside = end[:, 1] >= near
    crossing = start_inside != end_inside

    t = np.zeros(start.shape[0], dtype=float)
    np.divide(
        near - start[:, 1], end[:, 1] - start[:, 1],
        out=t, where=crossing,
    )
    intersection = start + t[:, None] * (end - start)
    intersection[:, 1] = near
    replace_start = crossing & ~start_inside
    replace_end = crossing & ~end_inside
    clipped[replace_start, 0] = intersection[replace_start]
    clipped[replace_end, 1] = intersection[replace_end]
    return clipped


segments = np.array([
    [[-40.0, 20.0], [40.0, 80.0]],
    [[-30.0, -20.0], [30.0, 0.0]],
    [[-40.0, -20.0], [80.0, 100.0]],
    [[80.0, 100.0], [-40.0, -20.0]],
    [[10.0, 30.0], [10.0, 30.0]],
])
before = segments.copy()
loop_result = clip_loop(segments, 30.0)
numpy_result = clip_numpy(segments, 30.0)
assert np.allclose(loop_result, numpy_result)
assert (numpy_result[:, :, 1] >= 30).all()
assert np.allclose(segments, before)
print(np.round(numpy_result, 2))
print(numpy_result.shape)

empty = np.zeros((0, 2, 2))
assert clip_loop(empty, 30.0).shape == (0, 2, 2)
assert clip_numpy(empty, 30.0).shape == (0, 2, 2)
hidden = segments[1:2]
assert clip_loop(hidden, 30.0).shape == (0, 2, 2)
assert clip_numpy(hidden, 30.0).shape == (0, 2, 2)
print("All clipping checks passed.")
