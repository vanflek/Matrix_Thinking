import numpy as np

# Each row stores the coordinates of one vertex: [x, y].
vertices = np.array([
    [-80, -50],
    [80, -50],
    [0, 70],
], dtype=float)

# Each row stores the indices of two connected vertices.
edges = np.array([
    [0, 1],
    [1, 2],
    [2, 0],
], dtype=int)

print("Vertices:", vertices.shape)
print("Edges:", edges.shape)

# Retrieve both endpoints of each edge.
for start_index, end_index in edges:
    start_point = vertices[start_index]
    end_point = vertices[end_index]
    print(start_index, end_index, start_point, end_point)
