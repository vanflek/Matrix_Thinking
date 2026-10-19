import numpy as np

# Represent the same point as a column and as a row.
point_column = np.array([
    [2],
    [3],
    [1],
], dtype=float)
point_row = point_column.T

# This matrix was written for a point-column.
transform_matrix = np.array([
    [1, 0, 5],
    [0, 1, -2],
    [0, 0, 1],
], dtype=float)

result_column = transform_matrix @ point_column
result_row = point_row @ transform_matrix.T

print("Column shape:", point_column.shape)
print("Row shape:", point_row.shape)
print("Column result:")
print(result_column)
print("Row result:")
print(result_row)

# Apply the same operation to several point-rows.
vertices = np.array([
    [2, 3, 1],
    [0, 0, 1],
    [-1, 4, 1],
], dtype=float)
transformed_vertices = vertices @ transform_matrix.T

print("All points:")
print(transformed_vertices)

# A one-dimensional array keeps its shape when transposed.
vector = np.array([2, 3, 1], dtype=float)
print("1D shape:", vector.shape)
print("1D transpose shape:", vector.T.shape)
