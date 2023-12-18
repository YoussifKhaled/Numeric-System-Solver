import numpy as np
from numpy import linalg as LA

class Doolitle:
    def __init__(self, a, b, sig_figs=20, tol=0.0001):
        self.a = a
        self.b = b
        self.sig_figs = sig_figs
        self.tol = tol
        self.steps = []
        self.l = None
        self.u = None
        self.x = None

    def ROUND_SIG(self, n, sig_figs):
        num = n
        counter = 0
        if num != 0:
            while (num >= 1 or num < -1):
                num = num / 10
                counter += 1
            num = round(num, sig_figs)
            num = num * 10 ** counter
            return num
        else:
            return 0.0

    def DecomposeEasier(self):
        self.steps = []  # reset steps
        n = len(self.a)
        l = np.zeros((n, n))
        u = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                u[i][j] = self.a[i][j]

        self.steps.append(
            f"Initialize L and U matrices:\nL = {l}\nU = {u}"
        )

        for i in range(n - 1):
            l[i][i] = 1
            for j in range(i + 1, n):
                factor = self.ROUND_SIG(u[j][i] / u[i][i], self.sig_figs)
                self.steps.append(
                    f"Calculate factor for row {j + 1}, column {i + 1}: {u[j][i]} / {u[i][i]} = {factor}"
                )
                l[j][i] = factor
                u[j][i] = 0

                self.steps.append(
                    f"Set L element ({j + 1}, {i + 1}) to {factor} and U element ({j + 1}, {i + 1}) to 0.\nL = {l}\nU = {u}"
                )

                for k in range(i + 1, n):
                    new_u_element = self.ROUND_SIG(
                        u[j][k] - self.ROUND_SIG(factor * u[i][k], self.sig_figs), self.sig_figs
                    )
                    self.steps.append(
                        f"Update U element ({j + 1}, {k + 1}): {u[j][k]} - {factor} * {u[i][k]} = {new_u_element}.\nU = {u}"
                    )
                    u[j][k] = new_u_element

        l[n - 1][n - 1] = 1

        self.steps.append(f"Final: Set L element ({n}, {n}) to 1.\nL = {l}")

        return l, u

    def substitute(self):
        n = len(self.b)
        x = np.zeros(n)
        y = np.zeros(n)

        self.steps.append(f"Initialize forward substitution vectors x and y.\nx = {x}\ny = {y}")

        for i in range(0, n):
            sum_val = self.b[i]
            for j in range(i):
                sum_val = self.ROUND_SIG(
                    sum_val - self.ROUND_SIG(self.l[i][j] * y[j], self.sig_figs), self.sig_figs
                )
                self.steps.append(
                    f"Forward substitution for row {i + 1}, update sum: {self.b[i]} - {self.l[i][j]} * {y[j]} = {sum_val}"
                )
            y[i] = self.ROUND_SIG(sum_val / self.l[i][i], self.sig_figs)
            self.steps.append(
                f"Calculate y element ({i + 1}): {sum_val} / {self.l[i][i]} = {y[i]}.\ny = {y}"
            )

        self.steps.append(f"Completed forward substitution, calculated y vector: {y}")

        x[n - 1] = self.ROUND_SIG(y[n - 1] / self.u[n - 1][n - 1], self.sig_figs)
        self.steps.append(
            f"Backward substitution, start with x element ({n}, {n}): {y[n - 1]} / {self.u[n - 1][n - 1]} = {x[n - 1]}.\nx = {x}"
        )

        for i in range(n - 2, -1, -1):
            sum_val = 0
            for j in range(i + 1, n):
                sum_val = self.ROUND_SIG(sum_val + self.ROUND_SIG(self.u[i][j] * x[j], self.sig_figs), self.sig_figs)
                self.steps.append(
                    f"Backward substitution, update sum for row {i + 1}: {sum_val} + {self.u[i][j]} * {x[j]}"
                )
            x[i] = self.ROUND_SIG(
                self.ROUND_SIG((y[i] - sum_val), self.sig_figs) / self.u[i][i], self.sig_figs
            )
            self.steps.append(
                f"Backward substitution, calculate x element ({i + 1}, {i + 1}): ({y[i]} - {sum_val}) / {self.u[i][i]} = {x[i]}.\nx = {x}"
            )

        return x

    def pivot(self, o, s, n, k):
        p = k
        big = self.ROUND_SIG(abs(self.a[int(o[k])][k] / s[int(o[k])]), self.sig_figs)
        for i in range(k + 1, n):
            dummy = self.ROUND_SIG(abs(self.a[int(o[i])][k] * s[int(o[i])]), self.sig_figs)
            if dummy > big:
                big = dummy
                p = i

        dummy = o[p]
        o[p] = o[k]
        o[k] = dummy
        return o

    def calculateError(self):
        return LA.norm(np.dot(self.l, self.u) - self.a)

    def isSquare(self, a):
        return all(len(row) == len(a) for row in a)

    def isSing(self, a):
        return LA.det(a) == 0

    def main(self):
        if self.isSquare(self.a):
            if not self.isSing(self.a):
                try:
                    self.l, self.u = self.DecomposeEasier()
                    self.steps.append(f"LU decomposition completed: L = {self.l} and U = {self.u}")

                    self.steps.append(f"Error calculated: ||A - LU|| = {self.calculateError()}")

                    self.x = self.substitute()
                    self.steps.append(f"Back substitution completed: x = {self.x}")

                    print("Final result:")
                    print("l = ", self.l)
                    print("u = ", self.u)
                    print("a= ", np.dot(self.l, self.u))
                    print("x = ", self.x)

                except ValueError as e:
                    raise ValueError("Error in the middle of calculations:", e)
            else:
                raise ValueError("a is singular")
        else:
            raise ValueError("a is not square")

# # Example usage:
# a = np.array([[1, 1, 2], [-1, -2, 3], [3, 7, 4]])
# b = np.array([8, 1, 10])
# lu_decomposition_instance = Doolitle(a, b)
# lu_decomposition_instance.main()
