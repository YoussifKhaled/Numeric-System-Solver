#fixed point iteration method
#input is non-linear equation (g(x)),precision,tol,initial guess,max iterations
import math
from math import *

def fixed_point(g, x0, precision, tol, max_iterations):

  f = lambda x: eval(g, {"x":x,"e":math.e ,"sin":math.sin,"cos":math.cos,"sqrt":math.sqrt})
  
  relativeError = 1
  count = 1
  steps = []

  while max_iterations != 0 and relativeError >= tol:

    x0 = round(x0, precision - len(str(int(x0))))
    x1 = f(x0)
    x1 = round(x1, precision - len(str(int(x1))))

    if abs(x1) > 1e20:  # Check for divergence
      steps.clear()
      steps.append("This system of equations will not converge.")
      return -1, steps

    if x1 != 0:
      relativeError = abs(x1 - x0) / abs(x1)


    step = f"iteration number {count}: x = {x1},relativeError = {round(relativeError*100,5)}%"
    steps.append(step)

    x0 = x1
    count += 1
    max_iterations -= 1

  if relativeError >= tol:
    steps.clear()
    steps.append("This system of equations will not converge")
    return -1, steps

  return x0, steps
  

result, steps = fixed_point("(x**2-3)/2", 1, 5, 0.001, 100)
print(result)

for step in steps:
  print(step)

