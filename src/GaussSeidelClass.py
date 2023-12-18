import copy

class GaussSeidelSolver:
    def __init__(self, matrix, initial_cond, iterations, tol, precision=5):
        self.matrix = matrix
        self.initial_cond = initial_cond
        self.iterations = iterations
        self.tol = tol
        self.precision = precision

    def remove_zero_diagonals(self):
        for i in range(len(self.matrix)):
            if self.matrix[i][i] == 0:
                if i == len(self.matrix) - 1:
                    values = i
                    for j in range(i - 1, -1, -1):
                        values -= 1
                        if self.matrix[j][i] != 0 and self.matrix[i][values] != 0:
                            self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                            break
                else:
                    for j in range(i + 1, len(self.matrix)):
                        if self.matrix[j][i] != 0:
                            self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                            break

    def gauss_seidel(self):
        self.remove_zero_diagonals()

        values = copy.deepcopy(self.initial_cond)
        relative_error = 1
        steps = []
        count = 1

        while self.iterations != 0 and relative_error >= self.tol:
            prev = copy.deepcopy(values)
            relative_error = 0

            for i in range(len(values)):
                numerator, denominator = (self.matrix[i][len(values)], 0)
                for j in range(len(values)):
                    if i != j:
                        numerator -= round(self.matrix[i][j] * values[j], self.precision - len(str(int(prev[j]))))
                    else:
                        denominator = self.matrix[i][j]

                if denominator == 0:
                    steps.append("Can't solve using Gauss-Seidel, diagonal elements are zero")
                    raise ValueError("Can't solve using Gauss-Seidel, diagonal elements are zero")
                else:
                    values[i] = round(numerator / denominator, self.precision - len(str(int(prev[i]))))

            for i in range(len(values)):
                if values[i] != 0:
                    error = abs(values[i] - prev[i]) / abs(values[i])
                    relative_error = max(relative_error, error)

            step = f"iteration number {count}: values = {values}, relative_error = {round(relative_error * 100, 5)}%"
            steps.append(step)
            self.iterations -= 1
            count += 1

        if relative_error >= self.tol:
            steps.clear()
            steps.append("This system of equations will not converge")
            return -1, steps

        return values, steps


# Example usage
matrix = [[2, 3, -1, 4, -1, 5, 6, 10],
          [1, 2, 3, -1, 4, 1, -5, 5],
          [3, 1, -2, 3, -4, 2, -1, 3],
          [4, 3, 1, 2, 0, 3, -6, 9],
          [1, -2, 3, 1, 2, -3, 4, -2],
          [2, -1, 4, 2, -1, 3, -2, 6],
          [3, 2, 2, -3, 4, -5, 6, -1]]

solver = GaussSeidelSolver(matrix, [0, 0, 0, 0, 0, 0, 0], 100, 0.0005, 5)
ans, steps = solver.gauss_seidel()

print(ans)
for step in steps:
    print(step)
