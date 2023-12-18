class JacobiSolver:
    def __init__(self, A, initial_guess, iterations, tol, precision=5):
        self.A = A
        self.initial_guess = initial_guess
        self.iterations = iterations
        self.tol = tol
        self.precision = precision

    def remove_zero_diagonals(self):
        for i in range(len(self.A)):
            if self.A[i][i] == 0:
                if i == len(self.A) - 1:
                    x = i
                    for j in range(i - 1, -1, -1):
                        x -= 1
                        if self.A[j][i] != 0 and self.A[i][x] != 0:
                            self.A[i], self.A[j] = self.A[j], self.A[i]
                            break
                else:
                    for j in range(i + 1, len(self.A)):
                        if self.A[j][i] != 0:
                            self.A[i], self.A[j] = self.A[j], self.A[i]
                            break

    def jacobi(self):
        self.remove_zero_diagonals()

        x = self.initial_guess
        relative_error = 1
        steps = []
        count = 1

        while (self.iterations != 0 and relative_error >= self.tol):
            temp = x.copy()
            relative_error = 0

            for i in range(len(x)):
                numerator, denominator = (self.A[i][len(x)], 0)
                for j in range(len(x)):
                    if (i != j):
                        numerator -= round(self.A[i][j] * temp[j],
                                           self.precision - len(str(int(temp[j]))))
                    else:
                        denominator = self.A[i][j]

                if denominator == 0:
                    raise ValueError("Can't solve using Jacobi, diagonal elements are zero")
                else:
                    x[i] = round(numerator / denominator,
                                 self.precision - len(str(int(temp[i]))))

            for i in range(len(x)):
                if x[i] != 0:
                    error = abs(x[i] - temp[i]) / abs(x[i])
                    relative_error = max(relative_error, error)

            step = f"Iteration number {count}: x = {x}, relativeError = {round(relative_error*100, 5)}%"
            steps.append(step)
            self.iterations -= 1
            count += 1

        return x, steps