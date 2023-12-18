from decimal import Decimal, getcontext

class GaussJordanElimination:
    def __init__(self, matrix, precision=5):
        self.matrix = matrix
        self.precision = precision
        self.steps = []
        self.dim = len(matrix)
        getcontext().prec = precision
        getcontext().rounding = 'ROUND_HALF_UP'

    def get_matrix(self, matrix):
        return [[float(element) for element in row] for row in matrix]

    def gauss_jordan_elimination(self):
        Infinite_flag = False

        matrix = [[Decimal(element) for element in row] for row in self.matrix]  # Converting to decimal
        dim = len(matrix)

        scaled_matrix = [row[:] for row in matrix]

        self.steps.append([self.get_matrix(matrix), "Original matrix"])

        # Scaling
        for row in range(dim):
            coef_max = max(abs(x) for x in matrix[row][:dim])  # maximum coeff in row
            if coef_max == Decimal('0'):
                if matrix[row][dim] != Decimal('0'):
                    raise ValueError("Matrix is inconsistent, No solution")
                else:
                    Infinite_flag = True
                    continue
            for col in range(dim + 1):
                scaled_matrix[row][col] /= coef_max
        self.steps.append([self.get_matrix(scaled_matrix), "Scaling the matrix"])

        # Solving
        for row in range(dim):

            # Pivoting
            indx_max = row  # index of row with max value
            val_max = abs(scaled_matrix[row][row])  # Value of current pivot
            for i in range(row + 1, dim):  # searching for max element below pivot to swap with pivot
                val_tmp = abs(scaled_matrix[i][row])
                if val_tmp > val_max:
                    val_max = val_tmp
                    indx_max = i

            # Swap rows
            if indx_max != row:
                matrix[row], matrix[indx_max] = matrix[indx_max], matrix[row]
                scaled_matrix[row], scaled_matrix[indx_max] = scaled_matrix[indx_max], scaled_matrix[row]
                self.steps.append([self.get_matrix(matrix),
                                   "Applying Pivoting (R{} <-> R{})".format(row + 1, indx_max + 1)])

            pivot = matrix[row][row]
            # divide row by pivot
            if pivot != Decimal('0'):
                for j in range(row, dim + 1):
                    matrix[row][j] /= pivot
                self.steps.append([self.get_matrix(matrix), "Dividing R{} by {}".format(row + 1, pivot)])

            # subtract scaled pivot row from other rows
            for i in range(dim):
                if i != row:
                    factor = matrix[i][row]
                    for j in range(row, dim + 1):
                        matrix[i][j] -= factor * matrix[row][j]
                    # Checking for consistency
                    val_max_check = max(abs(x) for x in matrix[i][:dim])
                    if val_max_check == Decimal('0'):
                        if matrix[i][dim] != Decimal('0'):
                            raise ValueError("Matrix is inconsistent, No solution")
                        else:
                            Infinite_flag = True
                            continue
                    if factor != Decimal('0'):
                        self.steps.append([self.get_matrix(matrix),
                                           "Adding ({})*R{} to R{}".format(-factor, row + 1, i + 1)])
        if Infinite_flag:
            raise ValueError("Infinite Solutions")
        # Solution
        values = [float(row[-1]) for row in matrix]

        return values, self.steps

    def getcontext(self):
        return getcontext()