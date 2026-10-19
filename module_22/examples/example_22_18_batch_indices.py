import numpy as np

start = 256
walls = np.array([
    [False, False, False],
    [False, True,  False],
    [True,  False, False],
])
has_wall = np.array([False, True, False])
end_index = np.array([999, 100, 999])
batch_has_wall = walls.any(axis=0)
new_hits = batch_has_wall & ~has_wall
first_hit = walls.argmax(axis=0)
end_index[new_hits] = start + first_hit[new_hits]
has_wall[new_hits] = True

print(first_hit)
print(new_hits)
print(end_index)
print(has_wall)
