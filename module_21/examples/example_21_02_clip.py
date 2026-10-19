import numpy as np

# A 107-unit margin leaves the center inside [-277, 277].
half_width = 768 / 2
margin = 107.0
min_x = -half_width + margin
max_x = half_width - margin

print(np.clip(300.0, min_x, max_x))
print(np.clip(-400.0, min_x, max_x))
print(np.clip(100.0, min_x, max_x))
