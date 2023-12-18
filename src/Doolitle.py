import numpy as np
from numpy import linalg as LA

steps = []


def ROUND_SIG(n, sig_figs):
    num = n
    counter = 0
    if num != 0:
        while (num >= 1 or num < -1):
            num = num / 10
            counter += 1
        num = round(num, sig_figs)
        num = num * 10 ** counter
        return num
    else:
        return 0.0


def Decompose(a, n, sig_figs):
    steps=[] #reset steps
    l = np.zeros((n, n))
    u = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            u[i][j] = a[i][j]

    steps.append(
        f"Initialize L and U matrices:\nL = {l}\nU = {u}"
    )

    for i in range(n - 1):
        l[i][i] = 1
        for j in range(i + 1, n):
            factor = ROUND_SIG(u[j][i] / u[i][i], sig_figs)
            steps.append(
                f"Calculate factor for row {j + 1}, column {i + 1}: {u[j][i]} / {u[i][i]} = {factor}"
            )
            l[j][i] = factor
            u[j][i] = 0

            steps.append(
                f"Set L element ({j + 1}, {i + 1}) to {factor} and U element ({j + 1}, {i + 1}) to 0.\nL = {l}\nU = {u}"
            )

            for k in range(i + 1, n):
                new_u_element = ROUND_SIG(
                    u[j][k] - ROUND_SIG(factor * u[i][k], sig_figs), sig_figs
                )
                steps.append(
                    f"Update U element ({j + 1}, {k + 1}): {u[j][k]} - {factor} * {u[i][k]} = {new_u_element}.\nU = {u}"
                )
                u[j][k] = new_u_element

    l[n - 1][n - 1] = 1

    steps.append(f"Final: Set L element ({n}, {n}) to 1.\nL = {l}")

    return l, u


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

def pivot(a,b,s,n,k):
    p=k
    big=abs((a[k][k])/(s[k]))
    for  i in range(k+1,n):
        temp=abs((a[i][k])/(s[i]))
        if temp > big:
           big=temp
           p=i
    if p !=k:
        # swap row p & row k
        for j in range(k,n):
            temp= a[p][j]
            a[p][j]=a[k][j]
            a[k][j]=temp
        # swap b[p] & b[k]
        temp=b[p]
        b[p]=b[k]
        b[k]=temp
        # swap s[p] & s[k]
        temp=s[p]
        s[p]=s[k]
        s[k]=temp
        steps.append([
                      "applying Pivoting ("+"R"+str(p+1)+"<->"+"R"+str(k+1)+")"])
def pivot(a, o, s, n, k, sig_figs):
    p = k
    big = ROUND_SIG(abs(a[int(o[k])][k] / s[int(o[k])]), sig_figs)
    for i in range(k + 1, n):
        dummy = ROUND_SIG(abs(a[int(o[i])][k] * s[int(o[i])]), sig_figs)
        if dummy > big:
            big = dummy
            p = i

    dummy = o[p]
    o[p] = o[k]
    o[k] = dummy
    return o


def calculateError(a, l, u):
    # print(a)
    # print(np.dot(l, u))

    return LA.norm(np.dot(l, u) - a)


def isSquare(a):
    return all(len(row) == len(a) for row in a)


def isSing(a):
    return LA.det(a) == 0


def main():
    a = np.array([[1, 1, 2], [-1, -2, 3], [3, 7, 4]])
    b = np.array([8, 1, 10])
    x = np.zeros(len(b))
    sig_figs = 20  # Specify the number of significant figures
    tol = 0.0001
    if isSquare(a):
        if not isSing(a):
            try:
                l, u = Decompose(a, len(a), sig_figs)
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
                raise ValueError("Error in the middle of calculations:", e)
        else:
            raise ValueError("a is singular")
    else:
        raise ValueError("a is not square")


if __name__ == "__main__":
    main()
    # print (steps)