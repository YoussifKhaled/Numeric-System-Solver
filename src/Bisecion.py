import math
steps = []

def round_fig(x, n):
    return round(x, n - len(str(int(x))))

def bisection_method(func, a, b, tolerance,sig_fig,max_iter=50)  :
    steps.clear() 
    steps.append(f"a is {a} b is {b} tolerance is {tolerance} sig_fig is {sig_fig} before ")
    a = round_fig(a, sig_fig)
    b = round_fig(b, sig_fig)
    fb = round_fig(func(b), sig_fig)
    fa = round_fig(func(a), sig_fig)

    if fa * fb >= 0:
        raise ValueError("The function values at the interval endpoints must have opposite signs.")
    prev_c = 1000000
    error=100
    steps.append(f"Step 0: Interval is: [{a}, {b}] and initial Xr is {round_fig((a + b) / 2,sig_fig)}")
    
    for i in range(max_iter):
        c = round_fig((a + b) / 2,sig_fig)
        fa = round_fig(func(a),sig_fig)
        fb = round_fig(func(b),sig_fig)
        fc = round_fig(func(c),sig_fig)
        steps.append(f"function of a is {fa} function of b is {fb} function of c is {fc} ")


        if fc== 0:
            print(f"here sub with {c} with function equals {func(c)}")
            steps.append(f"Step {i+1}: Approximate root found: {c}")
            return c
        
        if error < tolerance:
            steps.append(f"Step {i+1}: Approximate root found: {c}")
            return c
        
        if(prev_c==1000000):
            error=100
        elif(c!=0):
            error=round_fig(abs(((c-prev_c)/c)*100),sig_fig)
        else:
            error=round_fig(abs(((c-prev_c))*100),sig_fig)
        steps.append(f"Step {i+1}: Interval updated: [{a}, {b}] Xr is {c} and Error is {error}")
        

        if fa * fc < 0:
            b = c
        elif fa * fc > 0:
            a = c
        else:
            if fa == 0:
                steps.append(f"Step {i+1}: Approximate root found: {a}")
                return a
            else:
                steps.append(f"Step {i+1}: Approximate root found: {b}")
                return b
            
        prev_c = c
    steps.clear()
    raise ValueError("The method did not converge")


def main(func_str, a, b, tolerance,sig_fig,max_iter=50):
    
    def f(x):
        return eval(func_str)
    
    try:
        root = bisection_method(f, a, b,tolerance,sig_fig,max_iter)
        print("Steps:")
        for step in steps:
            print(step)
        print("Root:", root)
        return steps,root

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
