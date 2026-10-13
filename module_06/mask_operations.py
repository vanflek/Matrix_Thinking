import numpy as np

# Keep data and the coordinate matrices separate.
matrix = np.zeros((3, 4), dtype=np.uint8)
row_indices, col_indices = np.indices(matrix.shape)
top = row_indices == 0
left = col_indices == 0

print("Top row:")
print(top)
print("Left column:")
print(left)
print("Union:")
print(top | left)
print("Intersection:")
print(top & left)
print("Outside their union:")
print(~(top | left))

# A False mask entry leaves the corresponding data unchanged.
matrix.fill(0)
matrix[top | left] = 1
print("Values selected by the union:")
print(matrix)
