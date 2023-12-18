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
        print(f"number is {num}")
        return num
    else:
        return 0.0
    
def Crout(a, sig_figs):
    steps = []  # Initialize an empty list to store steps
    n = len(a)
    l = np.zeros((n, n))
    u = np.zeros((n, n))

    # Step 1: Initialize diagonal elements of U to 1
    for k in range(n):
        u[k][k] = 1
        steps.append(f"Set U[{k}][{k}] = 1")

    # Step 2: Forward elimination
    for k in range(n):
        # Calculate temporary sum for L elements
        # print(f"in Step {k + 1}:")
        for i in range(0,k+1):
            # tmp_sum += ROUND_SIG(l[i][j] * u[j][k], sig_figs)
            l[k][i] = a[k][i] - np.dot(l[k, :i], u[:i, i])
            # print(f"l[{k+1}][{i+1}] = a[{k+1}][{i+1}]({a[k][i]}) - {np.dot(l[k, :i], u[:i, k])}")
            steps.append(f"l[{k+1}][{i+1}] = a[{k+1}][{i+1}]({a[k][i]}) - {np.dot(l[k, :i], u[:i, k])}")
        for j in range(1+k,n):
            # Calculate L element
            u[k][j] = (a[k][j] - np.dot(l[k, :k], u[:k, j])) / l[k][k]
            # print(f"u[{k+1}][{j+1}] = (a[{k+1}][{j+1}]({a[k][j]}) - {np.dot(l[k, :k], u[:k, j])}) / L[{k+1}][{k+1}]({l[k][k]})")
            steps.append(f"u[{k+1}][{j+1}] = (a[{k+1}][{j+1}]({a[k][j]}) - {np.dot(l[k, :k], u[:k, j])}) / L[{k+1}][{k+1}]({l[k][k]})")
            # print("l = ", l)
            # print("u = ", u)
            # print()
        steps.append(f"l = {l}")
        steps.append(f"u = {u}")
    return l, u, steps




def substitute(l, u, b, sig_figs):
    n = len(b)
    x = np.zeros(n)
    y = np.zeros(n)

    steps.append(f"Initialize forward substitution vectors x and y.\nx = {x}\ny = {y}")

    for i in range(0, n):
        sum = b[i]
        for j in range(i):
            sum = ROUND_SIG(
                sum - ROUND_SIG(l[i][j] * y[j], sig_figs), sig_figs
            )
            steps.append(
                f"Forward substitution for row {i + 1}, update sum: {b[i]} - {l[i][j]} * {y[j]} = {sum}"
            )
        y[i] = ROUND_SIG(sum / l[i][i], sig_figs)
        steps.append(
            f"Calculate y element ({i + 1}): {sum} / {l[i][i]} = {y[i]}.\ny = {y}"
        )

    steps.append(f"Completed forward substitution, calculated y vector: {y}")


    x[n - 1] = ROUND_SIG(y[n - 1] / u[n - 1][n - 1], sig_figs)
    steps.append(
        f"Backward substitution, start with x element ({n}, {n}): {y[n - 1]} / {u[n - 1][n - 1]} = {x[n - 1]}.\nx = {x}"
    )

    for i in range(n - 2, -1, -1):
        sum = 0
        for j in range(i + 1, n):
            sum = ROUND_SIG(sum + ROUND_SIG(u[i][j] * x[j], sig_figs), sig_figs)
            steps.append(
                f"Backward substitution, update sum for row {i + 1}: {sum} + {u[i][j]} * {x[j]}"
            )
        x[i] = ROUND_SIG(
            ROUND_SIG((y[i] - sum), sig_figs) / u[i][i], sig_figs
        )
        steps.append(
            f"Backward substitution, calculate x element ({i + 1}, {i + 1}): ({y[i]} - {sum}) / {u[i][i]} = {x[i]}.\nx = {x}"
        )

    return x

def calculateError(a, l, u):
    print(a)
    print(np.dot(l,u))
    
    return LA.norm(np.dot(l,u)-a)

def isSquare(a):
    return all(len(row) == len(a) for row in a)

def isSing(a, sig_figs):
    return ROUND_SIG(LA.det(a),sig_figs) == 0

def main():
    a = np.array([[1, 1, 2], [-1, -2, 3], [3, 7, 4]])
    b = np.array([8,1,10])
    sig_figs = 20  # Specify the number of significant figures
    if isSquare(a):
        if not isSing(a,sig_figs):
            try:
                l, u = Crout(a, sig_figs)
                steps.append(f"LU decomposition completed: L = {l} and U = {u}")


                steps.append(f"Error calculated: ||A - LU|| = {calculateError(a, l, u)}")

                x = substitute(l, u, b, sig_figs)
                steps.append(f"Back substitution completed: x = {x}")
               
                print("Final result:")
                print("l = ", l)
                print("u = ", u)
                print("a= ",np.dot(l,u))
                print("x = ", x)
            except ValueError as e:
                raise ValueError("Error:", str(e))
        else:
            raise ValueError("a is singular")
    else:
        raise ValueError("a is not square")




main()