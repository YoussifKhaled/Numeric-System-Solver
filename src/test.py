import numpy as np

def separate_augmented_matrix(augmented_matrix):
    if not isinstance(augmented_matrix, list):
        raise ValueError("Input must be a Python list")

    if not all(isinstance(row, list) for row in augmented_matrix):
        raise ValueError("Each row of the input must be a Python list")

    rows = len(augmented_matrix)

    if rows == 0:
        raise ValueError("Input matrix must have non-zero rows")

    cols_set = set(len(row) for row in augmented_matrix)
    if len(cols_set) != 1:
        raise ValueError("Invalid input matrix. Each row must have the same number of columns")

    num_cols_A = cols_set.pop() - 1

    A = np.array([row[:num_cols_A] for row in augmented_matrix])
    b = np.array([row[-1] for row in augmented_matrix])

    return A, b

# Example usage:
augmented_matrix_list = [[1, 2, 3, 4],
                         [5, 6, 7, 8],
                         [9, 10, 11, 12]]

A, b = separate_augmented_matrix(augmented_matrix_list)

print("Matrix A:")
print(A)

print("\nVector b:")
print(b)
