from decimal import Decimal, getcontext

class GaussJordanElimination:
    def __init__(self, matrix, precision=5):
        self.matrix = matrix
        self.precision = precision
        self.steps = []
        self.dim = len(matrix)
        self.getcontext().prec = precision
        self.getcontext().rounding = 'ROUND_HALF_UP'

    def get_matrix(self, matrix):
        return [[float(element) for element in row] for row in matrix]

    def solve(self):
        matrix = [[Decimal(element) for element in row] for row in self.matrix]
        dim = self.dim
        scaled_matrix = [row[:] for row in matrix]

        self.steps.append([self.get_matrix(matrix), "Original matrix"])

        for row in range(dim):
            coef_max = max(abs(x) for x in matrix[row][:dim])
            if coef_max == Decimal('0'):
                if matrix[row][dim] != Decimal('0'):
                    raise ValueError("Matrix is inconsistent, No solution")
                else:
                    raise ValueError("Infinite solutions")
            for col in range(dim + 1):
                scaled_matrix[row][col] /= coef_max
        self.steps.append([self.get_matrix(scaled_matrix), "Scaling the matrix"])

        for row in range(dim):
            indx_max = row
            val_max = abs(scaled_matrix[row][row])

            for i in range(row + 1, dim):
                val_tmp = abs(scaled_matrix[i][row])
                if val_tmp > val_max:
                    val_max = val_tmp
                    indx_max = i

            if indx_max != row:
                matrix[row], matrix[indx_max] = matrix[indx_max], matrix[row]
                scaled_matrix[row], scaled_matrix[indx_max] = scaled_matrix[indx_max], scaled_matrix[row]
                self.steps.append([self.get_matrix(matrix), f"Applying Pivoting (R{row + 1} <-> R{indx_max + 1})"])

            pivot = matrix[row][row]

            if pivot != Decimal('0'):
                for j in range(row, dim + 1):
                    matrix[row][j] /= pivot
                self.steps.append([self.get_matrix(matrix), f"Dividing R{row + 1} by {pivot}"])

            for i in range(dim):
                if i != row:
                    factor = matrix[i][row]
                    for j in range(row, dim + 1):
                        matrix[i][j] -= factor * matrix[row][j]

                    val_max_check = max(abs(x) for x in matrix[i][:dim])
                    if val_max_check == Decimal('0'):
                        if matrix[i][dim] != Decimal('0'):
                            raise ValueError("Matrix is inconsistent, No solution")
                        else:
                            raise ValueError("Infinite solutions")

                    if factor != Decimal('0'):
                        self.steps.append([self.get_matrix(matrix), f"Adding ({-factor})*R{row + 1} to R{i + 1}"])

        values = [float(row[-1]) for row in matrix]
        return values, self.steps

    def getcontext(self):
        return getcontext()

# # Example usage
# A = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
# solver = GaussJordanElimination(A, 5)
# ans, steps = solver.solve()

# print(ans)
# for step in steps:
#     print(step[1])
#     for row in step[0]:
#         print(row)
