import numpy as np

start = np.array([-4.0, -2.0])
end = np.array([8.0, 10.0])
near = 1.0
t = (near - start[1]) / (end[1] - start[1])
intersection = start + t * (end - start)
intersection[1] = near

print(t)
print(intersection)
