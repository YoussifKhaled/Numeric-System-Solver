from decimal import Decimal, getcontext

class GaussElimination:
    def __init__(self, matrix, precision=5):
        getcontext().rounding = 'ROUND_HALF_UP'
        self.steps = []
        self.matrix = matrix
        self.precision = precision
        getcontext().prec = precision

    def print_matrix(self, matrix):
        for row in matrix:
            print([float(element) for element in row])

    def get_matrix(self, a, b):
        return [[float(element) for element in row] + [float(constant)] for row, constant in zip(a, b)]

    def solve(self):
        matrix = [[Decimal(element) for element in row] for row in self.matrix]
        a = [row[:-1] for row in matrix]
        b = [row[-1] for row in matrix]
        n = len(a)

        self.steps.append([self.get_matrix(a, b), "Original matrix"])
        s = self.scaling(a, b, n)

        if s != -1 and s != -2:
            er = self.eliminate(a, b, s, n, tol=1e-12)
            if er != -1 and er != -2:
                return self.substitute(a, b, n), self.steps
            elif er == -1:
                raise ValueError("Infinite solutions")
            else:
                raise ValueError("No solutions")
        elif s == -1:
            raise ValueError("Infinite solutions")
        else:
            raise ValueError("No solutions")

    def scaling(self, a, b, n):
        s = [0] * n
        for i in range(0, n):
            s[i] = abs(a[i][0])
            for j in range(1, n):
                if abs(a[i][j]) > s[i]:
                    s[i] = abs(a[i][j])
            if s[i] == Decimal('0'):
                if b[i] == Decimal('0'):
                    return -1
                else:
                    return -2
        return s

    def pivot(self, a, b, s, n, k):
        p = k
        big = abs((a[k][k]) / (s[k]))
        for i in range(k + 1, n):
            temp = abs((a[i][k]) / (s[i]))
            if temp > big:
                big = temp
                p = i
        if p != k:
            for j in range(k, n):
                temp = a[p][j]
                a[p][j] = a[k][j]
                a[k][j] = temp
            temp = b[p]
            b[p] = b[k]
            b[k] = temp
            temp = s[p]
            s[p] = s[k]
            s[k] = temp
            self.steps.append([self.get_matrix(a, b),
                               f"Applying Pivoting (R{p + 1} <-> R{k + 1})"])

    def eliminate(self, a, b, s, n, tol):
        for k in range(0, n - 1):
            self.pivot(a, b, s, n, k)
            if abs((a[k][k]) / (s[k])) < tol:
                if b[k] == Decimal('0'):
                    return -1
                else:
                    return -2
            for i in range(k + 1, n):
                factor = (a[i][k]) / (a[k][k])
                for j in range(0, n):
                    a[i][j] = (a[i][j]) - ((factor) * (a[k][j]))
                b[i] = (b[i]) - (factor) * (b[k])
                self.steps.append([self.get_matrix(a, b),
                                   f"Add(R{i + 1} + {-float(factor)} * R{k + 1})"])

        if abs(a[n - 1][n - 1] / (s[n - 1])) < tol:
            if b[n - 1] == Decimal('0'):
                return -1
            else:
                return -2

    def substitute(self, a, b, n):
        x = [0] * n
        x[n - 1] = (b[n - 1]) / (a[n - 1][n - 1])
        self.steps.append([[], f"value of x{n} = {float(b[n - 1])} / {float(a[n - 1][n - 1])} = {float(x[n - 1])}"])
        for i in range(n - 2, -1, -1):
            _sum = 0
            for j in range(i + 1, n):
                _sum = _sum + (a[i][j]) * (x[j])
            x[i] = ((b[i]) - _sum) / (a[i][i])
            self.steps.append([[], f"value of x{i + 1} = {float(b[i])} - {_sum} / {float(a[i][i])} = {float(x[i])}"])
        return x


# # Example usage
A = [[1.0, 0.0, 0.0, 10.0],
[0.0, 1.0, 0.0, 11.0],
[0.0, 0.0, 1.0, 12.0]
]
solver = GaussElimination(A, 1)
ans, steps = solver.solve()

print(ans)
for step in steps:
    print(step[1])
    for row in step[0]:
        print(row)
