import copy
from math import floor
from math import log10


class GaussSeidelSolver:
    def __init__(self, matrix, tol, precision, initial_cond, max_iterations):
        self.matrix = matrix
        self.tol = tol
        self.precision = precision
        self.initial_cond = initial_cond
        self.max_iterations = max_iterations
        self.num_of_var = len(initial_cond)
        self.iterations = 0
        self.steps = []
        self.error = []
        self.max_error = 100

    def remove_zero_diagonals(self):
        for i in range(len(self.matrix)):
            if self.matrix[i][i] == 0:
                if i == len(self.matrix) - 1:
                    x = i
                    for j in range(i - 1, -1, -1):
                        x -= 1
                        if self.matrix[j][i] != 0 and self.matrix[i][x] != 0:
                            self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                            break
                else:
                    for j in range(i + 1, len(self.matrix)):
                        if self.matrix[j][i] != 0:
                            self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                            break

    def precise(self, x, precision):
        x = float(x)
        return round(x, -int(floor(log10(abs(x)))) + (precision - 1))

    def gauss_seidel(self):
        self.remove_zero_diagonals()
        values = copy.deepcopy(self.initial_cond)

        while (self.max_error > self.tol) and (self.iterations < self.max_iterations):
            self.error.clear()
            self.iterations += 1
            prev = copy.deepcopy(values)

            for i in range(self.num_of_var):
                result = 0
                for j in range(self.num_of_var + 1):
                    if (i != j) and (j != self.num_of_var):
                        result = self.precise(result + self.precise((-1) * values[j] * self.matrix[i][j],
                                                                      self.precision), self.precision)
                    if j == self.num_of_var:
                        result = self.precise(result + self.matrix[i][j], self.precision)
                for j in range(self.num_of_var):
                    if (i == j) and (self.matrix[i][j] != 0):
                        result = self.precise(result / self.matrix[i][j], self.precision)
                    elif (i == j) and (self.matrix[i][j] == 0):
                        self.steps.append("Can't solve using Gauss-Seidel, diagonals elements are zero")
                        raise ValueError("Can't solve using Gauss-Seidel, diagonals elements are zero")
                        return -1, self.steps
                values[i] = result

            if self.iterations != 1:
                for i in range(self.num_of_var):
                    e = self.precise(abs((values[i] - prev[i]) / values[i]), self.precision)
                    self.error.append(e)
                self.max_error = max(self.error, key=lambda x: x)
                step = f"iteration number {self.iterations}: x = {values}, relative error = " \
                       f"{self.precise(self.max_error * 100, self.precision)}%"
                self.steps.append(step)
            elif self.iterations == 1:
                step = f"iteration number {self.iterations}: x = {values}, relative error = -"
                self.steps.append(step)

        if (self.max_error > self.tol) and (self.iterations >= self.max_iterations):
            raise ValueError("Does not converge")
        else:
            return values, self.steps


# Example usage
solver = GaussSeidelSolver(matrix=[[10, 2, 3, 1], [1, 6, 2, 2], [4, 8, 12, 3]], precision=7, tol=0.01,
                           initial_cond=[1, 1, 1], max_iterations=10000)
result, steps = solver.gauss_seidel()

if result is None:
    print("Does not converge")
else:
    print(result)
    for step in steps:
        print(step)
