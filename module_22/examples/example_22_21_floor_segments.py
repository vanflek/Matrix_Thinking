import numpy as np

starts = np.array([[0, 0], [30, 0], [60, 0]])
ends = np.array([[0, 90], [30, 90], [60, 90]])
segments = np.stack((starts, ends), axis=1)

print(starts.shape)
print(segments.shape)
print(segments)
print(segments[1, 0])
