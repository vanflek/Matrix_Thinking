import numpy as np

# Explicit shape and initial values.
print("zeros:")
print(np.zeros((3, 5), dtype=np.uint8))
print("ones:")
print(np.ones((3, 5), dtype=np.uint8))
print("full:")
print(np.full((3, 5), 1, dtype=np.uint8))

# The shape and dtype come from a template, but its values are not copied.
matrix = np.zeros((3, 5), dtype=np.uint8)
matrix[1, 2] = 1
print("original:")
print(matrix)
print("zeros_like:")
print(np.zeros_like(matrix))
print("ones_like:")
print(np.ones_like(matrix))

# empty does not initialize numerical values. Write every element first.
new_matrix = np.empty_like(matrix)
ROWS, COLS = new_matrix.shape
for row in range(ROWS):
    for col in range(COLS):
        new_matrix[row, col] = 0
print("empty_like, after explicit initialization:")
print(new_matrix)

# A matrix of ones is different from an identity matrix.
print("eye:")
print(np.eye(5, dtype=np.uint8))
print("identity:")
print(np.identity(5, dtype=np.uint8))

# Each component keeps its position when placed on the main diagonal.
vector = np.array([1, 0, 1, 0, 1], dtype=np.uint8)
print("diag:")
print(np.diag(vector))

# tri creates ones; tril and triu preserve existing values in one region.
print("tri:")
print(np.tri(5, 5, dtype=np.uint8))
matrix = np.array([[1, 0, 1], [0, 1, 1], [1, 0, 1]], dtype=np.uint8)
print("tril:")
print(np.tril(matrix))
print("triu:")
print(np.triu(matrix))
print("original is unchanged:")
print(matrix)
