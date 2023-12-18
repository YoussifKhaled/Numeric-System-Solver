import copy
from math import floor
from math import log10


def remove_zero_diagonals(A):
    for i in range(len(A)):
        if A[i][i] == 0:
            if i == len(A) - 1:
                x = i
                for j in range(i - 1, -1, -1):
                    x -= 1
                    if A[j][i] != 0 and A[i][x] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
            else:
                for j in range(i + 1, len(A)):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break


def precise(x, precision):
    x = float(x)
    precision = int(precision)
    return round(x, -int(floor(log10(abs(x)))) + (precision - 1))


def gauss_seidel(matrix, tol, precision, initial_cond, max_iterations):
    remove_zero_diagonals(matrix)
    values = copy.deepcopy(initial_cond)
    num_of_var = len(initial_cond)
    iterations = 0
    steps = []
    error = []
    max_error = 100
    while (max_error > tol) and (iterations < max_iterations):
        error.clear()
        iterations += 1
        prev = copy.deepcopy(values)
        for i in range(num_of_var):
            result = 0
            for j in range(num_of_var + 1):
                if (i != j) and (j != num_of_var):
                    result = precise(result + precise((-1) * values[j] * matrix[i][j], precision), precision)
                if j == num_of_var:
                    result = precise(result + matrix[i][j], precision)
            for j in range(num_of_var):
                if (i == j) and (matrix[i][j] != 0):
                    result = precise(result / matrix[i][j], precision)
                elif (i == j) and (matrix[i][j] == 0):
                    steps.append("Can't solve using Gauss-Seidel, diagonals elements are zero")
                    return -1, steps
            values[i] = result

        if iterations != 1:
            for i in range(num_of_var):
                e = precise(abs((values[i] - prev[i]) / values[i]), precision)
                error.append(e)
            max_error = max(error, key=lambda x: x)
            step = f"iteration number {iterations}: x = {values}, relative error = {precise(max_error * 100, precision)}%"
            steps.append(step)
        elif iterations == 1:
            step = f"iteration number {iterations}: x = {values}, relative error = -"
            steps.append(step)

    if (max_error > tol) and (iterations >= max_iterations):
        return None
    else:
        return values, steps
