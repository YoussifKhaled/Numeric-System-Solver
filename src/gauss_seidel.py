# switch rows that have a zero in the diagonal element
import copy


def remove_zero_diagonals(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            if i == len(matrix) - 1:
                values = i
                for j in range(i - 1, -1, -1):
                    values -= 1
                    if matrix[j][i] != 0 and matrix[i][values] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
            else:
                for j in range(i + 1, len(matrix)):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break


def jacobi(matrix, initial_cond, iterations, tol, precision=5):
    remove_zero_diagonals(matrix)

    values = copy.deepcopy(initial_cond)
    relative_error = 1
    steps = []
    count = 1

    while iterations != 0 and relative_error >= tol:
        prev = copy.deepcopy(values)
        relative_error = 0

        for i in range(len(values)):
            numerator, denominator = (matrix[i][len(values)], 0)
            for j in range(len(values)):
                if (i != j):
                    numerator -= round(matrix[i][j] * values[j], precision - len(str(int(prev[j]))))
                else:
                    denominator = matrix[i][j]

            if denominator == 0:
                steps.append("Can't solve using gauss-seidel, diagonals elements are zero")
                return -1, steps
            else:
                values[i] = round(numerator / denominator, precision - len(str(int(prev[i]))))

        for i in range(len(values)):
            if values[i] != 0:
                error = abs(values[i] - prev[i]) / abs(values[i])
                relative_error = max(relative_error, error)

        step = f"iteration number {count}: values = {values},relative_error = {round(relative_error * 100, 5)}%"
        steps.append(step)
        iterations -= 1
        count += 1

    if relative_error >= tol:
        steps.clear()
        steps.append("This system of equations will not converge")
        return -1, steps

    return values, steps


matrix = [[10,0,1,4],
          [1,7,3,-1],
          [3,1,9,3]
          ]

ans, steps = jacobi(matrix, [0, 0, 0], 100, 0.0005, 5)
print(ans)
for steps in steps:
    print(steps)
