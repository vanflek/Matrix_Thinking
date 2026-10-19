import numpy as np

active_rays = np.array([1, 4, 7, 9])
batch_has_wall = np.array([False, True, False, True])
first_hit = np.array([0, 3, 0, 1])
inside_last = np.array([True, True, False, True])
start = 256
end_index = np.full(10, 999, dtype=int)
has_wall = np.zeros(10, dtype=bool)

hit_rays = active_rays[batch_has_wall]
end_index[hit_rays] = start + first_hit[batch_has_wall]
has_wall[hit_rays] = True
keep_searching = ~batch_has_wall & inside_last
active_rays = active_rays[keep_searching]

print(hit_rays)
print(end_index[hit_rays])
print(keep_searching)
print(active_rays)
