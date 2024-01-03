import math
# import signal


# def signal_handler (signal, frame):
    
#     raise TimeoutError()

# signal.signal(signal.SIGINT, signal_handler)


# diverged = False
steps = []

def round_fig(x, n):
    return round(x, n - len(str(int(x))))

def bisection_method(func, a, b, tolerance,sig_fig,max_iter=200)  :
    steps.clear() # Clear the steps list
    # print(f"a is {a} b is {b} tolerance is {tolerance} sig_fig is {sig_fig} before ")
    a = round_fig(a, sig_fig)
    b = round_fig(b, sig_fig)
    # print(f"a is {a} b is {b} tolerance is {tolerance} sig_fig is {sig_fig} after ")
    if round_fig(func(a) * func(b),sig_fig) >= 0:
        raise ValueError("The function values at the interval endpoints must have opposite signs.")
    prev_c = 1000000
    # i=0
    error=100
    # while(True):
    for i in range(max_iter):
        c = round_fig((a + b) / 2,sig_fig)
        print(round_fig(abs(func(c)),sig_fig) )
        # if round_fig(abs(func(c)),sig_fig) < tolerance:

        if round_fig(abs(func(c)),sig_fig) == 0:
            steps.append(f"Step {i+1}: Approximate root found: {c}")
            return c
        
        if error < tolerance:
            steps.append(f"Step {i+1}: Approximate root found: {c}")
            return c
        
        # if prev_c == c:
            # raise TimeoutError()

        if round_fig(round_fig(func(a),sig_fig) * round_fig(func(c),sig_fig),sig_fig) < 0:
            b = c
        else:
            a = c
        steps.append(f"Step {i+1}: Interval updated: [{a}, {b}] Xr is {c} and Error is {error}")
        prev_c = c
        error=round_fig(abs(((c-prev_c)/c)*100),sig_fig)
        # i+=1
    steps.clear()
    raise ValueError("The method did not converge")

# # Example usage:
# def f(x):
#     return x**2 - 4

# root = bisection_method(f, 0, 3)
# print("Root:", root)

def main(func_str, a, b, tolerance,sig_fig):
    
    def f(x):
        return eval(func_str)
    
    try:
        root = bisection_method(f, a, b,tolerance,sig_fig)
        print("Steps:")
        for step in steps:
            print(step)
        print("Root:", root)

    except TimeoutError as e:
        print("The method did not converge")
    except ValueError as e:
        print("Error:", str(e))

func_str = input("Enter the function: ").replace('^', '**').lower().replace('e', 'math.e').replace(' ', '').replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('sqrt', 'math.sqrt')
a = float(input("Enter the first number: "))
b = float(input("Enter the second number: "))
tolerance = float(input("Enter the tolerance: "))
sig_fig = int(input("Enter the number of significant figures: "))
print(f"a is {a} b is {b} tolerance is {tolerance} sig_fig is {sig_fig} func_str is {func_str}")
main(func_str, a, b, tolerance,sig_fig)
