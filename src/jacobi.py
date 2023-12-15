def jacobi(A, initialGuess, iterations, tol, precision=5):
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

      x[i] = round(numerator / denominator, precision - len(str(int(temp[i]))))

    for i in range(len(x)):
      if x[i] != 0:
        error = abs(x[i] - temp[i]) / abs(x[i])
        relativeError = max(relativeError, error)

    step = f"iteration number {count}: x = {x},relativeError = {round(relativeError*100,5)}%"
    steps.append(step)
    iterations -= 1
    count += 1

  return x, steps


A = [
    [20, 3, 4, -5,-6],
    [6, 20, -8, 9,96],
    [10, 11, 40, 13,312],
    [14, 15, 16, 50,416]
]
ans, steps = jacobi(A, [0,0,0,0], 20, 0.001, 7)
print(ans)

for step in steps:
  print(step)
