import numpy as np
from numpy import linalg as LA

class CholeskySolver:
    def __init__(self, a, b, sig_figs=5):
        self.a = a
        self.b = b
        self.sig_figs = sig_figs
        self.steps = []
        self.l = None
        self.u = None
        self.x = None

    def ROUND_SIG(self, n):
        num = n
        counter = 0
        if num != 0:
            while (num >= 1 or num <= -1):
                num = num / 10
                counter = counter + 1
            num = round(num, self.sig_figs)
            num = num * 10 ** counter
            return num
        else:
            return 0.0

    def Cholesky(self):
        self.steps = []  # Initialize an empty list to store steps
        n = len(self.a)
        l = np.zeros((n, n))
        u = np.zeros((n, n))
        for i in range(n):
            for k in range(i + 1):
                tmp_sum = self.ROUND_SIG(sum(self.ROUND_SIG(l[k][j] * l[i][j]) for j in range(k)))
                if i == k:
                    l[i][k] = self.ROUND_SIG(np.sqrt(self.ROUND_SIG(self.a[i][i] - tmp_sum)))
                    u[k][i] = l[i][k]
                    self.steps.append(f"Step {i + 1}:")
                    self.steps.append(f"l[{i}][{k}] = sqrt(a[{i}][{i}] - {tmp_sum})")
                    self.steps.append(f"u[{k}][{i}] = l[{i}][{k}]")
                else:
                    l[i][k] = self.ROUND_SIG(self.ROUND_SIG(self.a[i][k] - tmp_sum) / self.ROUND_SIG(l[k][k]))
                    u[k][i] = l[i][k]
                    self.steps.append(f"Step {i + 1}:")
                    self.steps.append(f"l[{i}][{k}] = (a[{i}][{k}] - {tmp_sum}) / (u[{k}][{k}] * l[{i}][{k}])")
                    self.steps.append(f"u[{k}][{i}] = l[{i}][{k}]")

        return l, u

    def substitute(self, l, u, b):
        n = len(b)
        x = np.zeros(n)
        y = np.zeros(n)

        self.steps.append(
            f"Initialize forward substitution vectors x and y.\nx = {x}\ny = {y}"
        )

        for i in range(0, n):
            sum = self.b[i]
            for j in range(i):
                sum = self.ROUND_SIG(
                    sum - self.ROUND_SIG(l[i][j] * y[j])
                )
                self.steps.append(
                    f"Forward substitution for row {i + 1}, update sum: {self.b[i]} - {l[i][j]} * {y[j]} = {sum}"
                )
            y[i] = self.ROUND_SIG(sum / l[i][i])
            self.steps.append(
                f"Calculate y element ({i + 1}): {sum} / {l[i][i]} = {y[i]}.\ny = {y}"
            )

        self.steps.append(
            f"Completed forward substitution, calculated y vector: {y}"
        )

        x[n - 1] = self.ROUND_SIG(y[n - 1] / u[n - 1][n - 1])
        self.steps.append(
            f"Backward substitution, start with x element ({n}, {n}): {y[n - 1]} / {u[n - 1][n - 1]} = {x[n - 1]}.\nx = {x}"
        )

        for i in range(n - 2, -1, -1):
            sum = 0
            for j in range(i + 1, n):
                sum = self.ROUND_SIG(
                    sum + self.ROUND_SIG(u[i][j] * x[j])
                )
                self.steps.append(
                    f"Backward substitution, update sum for row {i + 1}: {sum} + {u[i][j]} * {x[j]}"
                )
            x[i] = self.ROUND_SIG(
                self.ROUND_SIG((y[i] - sum)) / u[i][i]
            )
            self.steps.append(
                f"Backward substitution, calculate x element ({i + 1}, {i + 1}): ({y[i]} - {sum}) / {u[i][i]} = {x[i]}.\nx = {x}"
            )
        for i in range(n):
            x[i] = self.ROUND_SIG(x[i])
        return x

    def isSymmetric(self):
        return np.array_equal(self.a, self.a.T)

    def isPositiveDefinite(self):
        return np.all(np.linalg.eigvals(self.a) > 0)

    def calculateError(self):
        return LA.norm(np.dot(self.l, self.u) - self.a)

    def isSquare(self):
        return all(len(row) == len(self.a) for row in self.a)

    def isSing(self):
        return self.ROUND_SIG(LA.det(self.a)) == 0

    def main(self):
        if self.isSquare():
            if not self.isSing():
                if self.isSymmetric():
                    if self.isPositiveDefinite():
                        try:
                            self.l, self.u = self.Cholesky()
                            self.steps.append(f"LU decomposition completed: L = {self.l} and U = {self.u}")

                            self.x = self.substitute(self.l, self.u, self.b)
                            self.steps.append(f"Back substitution completed: x = {self.x}")

                            print("Final result:")
                            print("l = ", self.l)
                            print("u = ", self.u)
                            print("a= ", np.dot(self.l, self.u))
                            print("x = ", self.x)

                        except ValueError as e:
                            raise ValueError("Error:", str(e))
                    else:
                        raise ValueError("a is not positive definite")
                else:
                    raise ValueError("a is not symmetric")
            else:
                raise ValueError("a is singular")
        else:
            raise ValueError("a is not square")


# Example usage:
a = np.array([[6, 15, 55],
              [15, 55, 225],
              [55, 225, 979]])
b = np.array([7, 3, 8])
cholesky_instance = CholeskySolver(a, b)
cholesky_instance.main()
