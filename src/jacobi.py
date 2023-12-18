#switch rows that have a zero in the diagonal element
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


def jacobi(A, initialGuess, iterations, tol, precision=5):

  remove_zero_diagonals(A)
  
  x = initialGuess
  relativeError = 1
  steps = []
  count = 1

  while (iterations != 0 and relativeError >= tol):
    temp = x.copy()
    relativeError = 0

    for i in range(len(x)):
      numerator, denominator = (A[i][len(x)], 0)
      for j in range(len(x)):
        if (i != j):
          numerator -= round(A[i][j] * temp[j],
                             precision - len(str(int(temp[j]))))
        else:
          denominator = A[i][j]

      if denominator == 0:
        steps.append("Cant't solve using jacobi, diagonals elements are zero")
        return -1, steps
      else:
        x[i] = round(numerator / denominator,
                     precision - len(str(int(temp[i]))))

    for i in range(len(x)):
      if x[i] != 0:
        error = abs(x[i] - temp[i]) / abs(x[i])
        relativeError = max(relativeError, error)

    step = f"iteration number {count}: x = {x},relativeError = {round(relativeError*100,5)}%"
    steps.append(step)
    iterations -= 1
    count += 1

  return x, steps
