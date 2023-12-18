import numpy as np
from numpy import linalg as LA

class CroutDecomposition:
    def __init__(self, a, b, sig_figs=20):
        self.a = a
        self.b = b
        self.sig_figs = sig_figs
        self.steps = []
        self.x = None

    def ROUND_SIG(self, n):
        num = n
        counter = 0
        if num != 0:
            while num >= 1 or num <= -1:
                num = num / 10
                counter = counter + 1
            num = round(num, self.sig_figs)
            num = num * 10 ** counter
            print(f"number is {num}")
            return num
        else:
            return 0.0

    def Croutdec(self):
        self.steps = []  # Initialize an empty list to store steps
        n = len(self.a)
        l = np.zeros((n, n))
        u = np.zeros((n, n))

        # Step 1: Initialize diagonal elements of U to 1
        for k in range(n):
            u[k][k] = 1
            self.steps.append(f"Set U[{k}][{k}] = 1")

        # Step 2: Forward elimination
        for k in range(n):
            # Calculate temporary sum for L elements
            for i in range(0, k + 1):
                tmp_sum = self.ROUND_SIG(np.dot(l[k, :i], u[:i, i]))
                l[k][i] = self.ROUND_SIG(self.a[k][i] - tmp_sum)
                self.steps.append(
                    f"l[{k+1}][{i+1}] = a[{k+1}][{i+1}]({self.a[k][i]}) - {tmp_sum}"
                )
            for j in range(1 + k, n):
                # Calculate L element
                tmp_sum = self.ROUND_SIG(np.dot(l[k, :k], u[:k, j]))
                u[k][j] = self.ROUND_SIG(
                    self.ROUND_SIG((self.a[k][j] - tmp_sum)) / l[k][k],
      
                )
                self.steps.append(
                    f"u[{k+1}][{j+1}] = (a[{k+1}][{j+1}]({self.a[k][j]}) - {tmp_sum}) / L[{k+1}][{k+1}]({l[k][k]})"
                )
            self.steps.append(f"l = {l}")
            self.steps.append(f"u = {u}")
        return l, u

    def substitute(self, l, u):
        n = len(self.b)
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

        return x

    def calculateError(self, l, u):
        print(self.a)
        print(np.dot(l, u))

        return LA.norm(np.dot(l, u) - self.a)

    def isSquare(self):
        return all(len(row) == len(self.a) for row in self.a)

    def isSing(self):
        return self.ROUND_SIG(LA.det(self.a)) == 0

    def crout(self):
        if self.isSquare():
            if not self.isSing():
                try:
                    l, u = self.Croutdec()
                    self.steps.append(
                        f"LU decomposition completed: L = {l} and U = {u}"
                    )

                    self.steps.append(
                        f"Error calculated: ||A - LU|| = {self.calculateError(l, u)}"
                    )

                    x = self.substitute(l, u)
                    self.steps.append(f"Back substitution completed: x = {x}")
                    self.x = x

                    print("Final result:")
                    print("l = ", l)
                    print("u = ", u)
                    print("a= ", np.dot(l, u))
                    print("x = ", x)
                except ValueError as e:
                    # ValueError(e)
                    print("Error in the middle of calculations:" + str(e))
            else:
                raise ValueError("a is singular")
        else:
            raise ValueError("a is not square")


# Example usage
a = np.array([[1, 1, 2], [-1, -2, 3], [3, 7, 4]])
b = np.array([8, 1, 10])

solver = CroutDecomposition(a, b)
solver.crout()

# Access the steps if needed
for step in solver.steps:
    print(step)
