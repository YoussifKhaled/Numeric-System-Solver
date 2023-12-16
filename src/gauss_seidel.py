import copy
from math import floor
from math import log10


def precise (x, precision):
    x = float(x)
    precision = int(precision)
    return round(x, -int(floor(log10(abs(x)))) + (precision - 1))

def gauss_seidel(matrix, tol, precision, initial_cond, max_iterations):
    values = copy.deepcopy(initial_cond)
    num_of_var = len(initial_cond)
    iterations = 0
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
                if i == j:
                    result = precise(result / matrix[i][j], precision)
            values[i] = result

        if iterations != 1:
            for i in range(num_of_var):
                e = precise(abs(( values[i] - prev[i] ) / values[i]), precision)
                error.append(e)
            max_error = max(error, key = lambda x:x)

    if (max_error > tol) and (iterations >= max_iterations):
        return None
    else:
        return values




xxxx = gauss_seidel(matrix=[[10, 2, 3, 1], [1, 6, 2, 2], [4, 8, 12, 3]], precision = 5, tol = 0.01 , initial_cond=[1, 1, 1], max_iterations = 10000)
if xxxx is None:
    print("Does not converge")
else:
    print(xxxx)
