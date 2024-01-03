import math
def round_fig(x, n):
    return round(x, n - len(str(int(x))))
steps = []
def false_position(f, a, b, tol, sig_fig,max_iter=200):
    
    steps.clear() # Clear the steps list
    fa = round_fig(f(a),sig_fig)
    fb = round_fig(f(b),sig_fig)

    if fa * fb >= 0:
        raise ValueError("The function values at the interval endpoints must have opposite signs.")
    error=100
    prev_c = 1000000
    # i=0
    # while(True):
    for i in range(max_iter):
        c = round_fig((a * fb - b * fa) / (fb - fa),sig_fig)
        fc = round_fig(f(c),sig_fig)

        # if abs(fc) < tol:
        if fc == 0:
            steps.append(f"Step {i+1}: Approximate root found: {c}")
            return c
        
        if error < tol:
            # raise TimeoutError()
            steps.append(f"Step {i+1}: Approximate root found: {c}")
            return c
        if prev_c == c:
            raise TimeoutError()
        if round_fig(fa * fc,sig_fig) < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        steps.append(f"Step {i+1}: Interval updated: [{a}, {b}] Xr is {c} and Error is {error}")
        prev_c = c
        error=round_fig(abs(((c-prev_c)/c)*100),sig_fig)
    # raise RuntimeError("The method did not converge within the maximum number of iterations.")


def main(func_str, a, b, tolerance,sig_fig):
    func_str=func_str.replace('^', '**').lower().replace('e', 'math.e').replace(' ', '').replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('sqrt', 'math.sqrt')
    def f(x):
        return eval(func_str)
    
    try:
        root = false_position(f, a, b,tolerance,sig_fig)
        print("Steps:")
        for step in steps:
            print(step)
        print("Root:", root)

    except TimeoutError as e:
        print("The method did not converge")
    except ValueError as e:
        print("Error:", str(e))

func_str = input("Enter the function: ")
a = float(input("Enter the first number: "))
b = float(input("Enter the second number: "))
tolerance = float(input("Enter the tolerance: "))
sig_fig = int(input("Enter the number of significant figures: "))
print(f"a is {a} b is {b} tolerance is {tolerance} sig_fig is {sig_fig} func_str is {func_str}")
    
main(func_str, a, b, tolerance,sig_fig)
