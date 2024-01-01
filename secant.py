import math


def secant(fstring, x0, x1, precision, tol, max_iterations):
    f = lambda x: eval(fstring, {"x": x, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                                 "exp": math.exp, "e^": math.exp, "log": math.log10, "ln": math.log,
                                 "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                                 "arcsin": math.asin, "arccos": math.acos, "arctan": math.atan,
                                 "arcsinh": math.asinh, "arccosh": math.acosh, "arctanh": math.atanh})

    relative_error = 1
    iterations = 1
    steps = []
    x0 = round(x0, precision - len(str(int(x0))))
    x1 = round(x1, precision - len(str(int(x1))))
    f0 = f(x0)
    f1 = f(x1)
    f0 = round(f0, precision - len(str(int(f0))))
    f1 = round(f1, precision - len(str(int(f1))))

    while max_iterations > iterations and relative_error >= tol:

        numerator = x1 - x0
        numerator = round(numerator, precision - len(str(int(numerator))))
        denominator = f1 - f0
        denominator = round(denominator, precision - len(str(int(denominator))))

        x2 = x1 - (f1 * (numerator / denominator))
        x2 = round(x2, precision - len(str(int(x2))))

        if x2 != 0 and iterations != 1:
            relative_error = abs(x2 - x1) / abs(x2)
            step = f"iteration number {iterations}: x = {x2}, relative_error = {round(relative_error * 100, 5)}%"
        elif iterations == 1:
            step = f"iteration number {iterations}: x = {x2}, relative_error = -"

        steps.append(step)

        x0 = x1
        x1 = x2
        f0 = f1
        f1 = f(x1)
        iterations += 1

    if relative_error >= tol:
        steps.clear()
        steps.append("This system of equations will not converge")
        return -1, steps

    return x2, steps

# result, steps = secant("x**3 - x**2 - 10*x + 7", 3, 3.5, 6, 0.0001, 100)
# print(result)
# for step in steps:
#   print(step)
