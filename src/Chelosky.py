import numpy as np
from numpy import linalg as LA

steps=[]

def ROUND_SIG(n, sig_figs):
    num=n
    counter=0
    if num != 0:
        while(num>=1 or num<=-1):
            num=num/10
            counter=counter+1
        num=round(num, sig_figs)
        num=num*10**counter
        return num
    else:
        return 0.0


# Define the Cholesky decomposition function
def Choleskydec(a, sig_figs):
    steps = []  # Initialize an empty list to store steps
    n = len(a)
    l = np.zeros((n, n))
    u = np.zeros((n, n))
    for i in range(n):
        for k in range(i + 1):
            tmp_sum = ROUND_SIG(sum(ROUND_SIG(l[k][j] * l[i][j], sig_figs) for j in range(k)), sig_figs)
            if i == k:
                l[i][k] = ROUND_SIG(np.sqrt(ROUND_SIG(a[i][i] - tmp_sum, sig_figs)), sig_figs)
                u[k][i] = l[i][k]
                steps.append(f"Step {i + 1}:")
                steps.append(f"l[{i}][{k}] = sqrt(a[{i}][{i}] - {tmp_sum})")
                steps.append(f"u[{k}][{i}] = l[{i}][{k}]")
                
            else:
                l[i][k] = ROUND_SIG(ROUND_SIG(a[i][k] - tmp_sum, sig_figs) / ROUND_SIG(l[k][k], sig_figs), sig_figs)
                u[k][i] = l[i][k]
                steps.append(f"Step {i + 1}:")
                steps.append(f"l[{i}][{k}] = (a[{i}][{k}] - {tmp_sum}) / (u[{k}][{k}] * l[{i}][{k}])")
                steps.append(f"u[{k}][{i}] = l[{i}][{k}]")
            
    return l, u

# Define the forward substitution function
def substitute(l, u, b, sig_figs):
    n = len(b)
    x = np.zeros(n)
    y = np.zeros(n)
    for i in range(n):
        sum = b[i]
        for j in range(i):
            sum = ROUND_SIG(sum - ROUND_SIG(l[i][j] * y[j], sig_figs), sig_figs)
        y[i] = ROUND_SIG(sum / l[i][i], sig_figs)
        steps.append(f"y[{i}] = (b[{i}] - {sum}) / l[{i}][{i}]")

    x[n - 1] = ROUND_SIG(y[n - 1] / u[n - 1][n - 1], sig_figs)
    steps.append(f"x[{n - 1}] = y[{n - 1}] / u[{n - 1}][{n - 1}]")
    for i in range(n - 2, -1, -1):
        sum = 0
        for j in range(i + 1, n):
            sum = ROUND_SIG(sum + ROUND_SIG(u[i][j] * x[j], sig_figs), sig_figs)
        x[i]=ROUND_SIG(ROUND_SIG((y[i]-sum), sig_figs)/u[i][i], sig_figs)
        steps.append(f"x[{i}]({x[i]}) = y[{i}]({y[i]}) - sum({sum}) / u[{i}][{i}]({u[i][i]}))")
        
    return x


def isSymmetric(a):
    return np.array_equal(a, a.T)

def isPositiveDefinite(a):
    return np.all(np.linalg.eigvals(a) > 0)

def calculateError(a, l, u):
    # print(a)
    # print(np.dot(l,u))
    return LA.norm(np.dot(l,u)-a)

def isSquare(a):
    return all(len(row) == len(a) for row in a)

def isSing(a,sig_figs):
    return ROUND_SIG(LA.det(a),sig_figs) == 0

def cholesky():
    a = np.array([[6, 15, 55],
                  [15, 55, 225],
                  [55, 225, 979]])
    b = np.array([7, 3, 8])
    sig_figs = 20  # Specify the number of significant figures
    if isSquare(a):
        if not isSing(a,sig_figs):
            if isSymmetric(a):
                if isPositiveDefinite(a):
                    try:
                        l, u = Choleskydec(a, sig_figs)
                        steps.append(f"LU decomposition completed: L = {l} and U = {u}")

                        # steps.append(f"Error calculated: ||A - LU|| = {calculateError(a, l, u)}")

                        x = substitute(l, u, b, sig_figs)
                        steps.append(f"Back substitution completed: x = {x}")

                        print("Final result:")
                        print("l = ", l)
                        print("u = ", u)
                        print("a= ",np.dot(l,u))
                        print("x = ", x)
                        # calculateError(a, l, u)

                    except ValueError as e:
                        raise ValueError("Error in the middle of calculations:", e)
                else:
                    raise ValueError("a is not positive definite")
            else:
                raise ValueError("a is not symmetric")
        else:
            raise ValueError("a is singular")
    else:
        raise ValueError("a is not square")

cholesky()
