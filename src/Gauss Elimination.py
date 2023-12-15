from decimal import Decimal,getcontext
getcontext().rounding='ROUND_HALF_UP'
steps=[]

def print_matrix(matrix):
    for row in matrix:
        print([float (element) for element in row])
def get_matrix(a,b):
    return [[float(element) for element in row] + [float(constant)] for row, constant in zip(a, b)]

#Gauss-Elimination 
# arguments
# matrix: Augmented Matrix 
# n: Number of equations, precision   
def gauss_elimination(matrix,n,precision):
    a = [row[:-1] for row in matrix] 
    b = [row[-1] for row in matrix]   
    getcontext().prec=precision
    x=[0]*n
    
    steps.append([get_matrix(a,b),"Original matrix"])
    s=scaling(a,n)
    if s != -1 :
       er=eliminate(a,b,s,n,tol=1e-12)
       if er != -1:
          substitute(a,b,n,x)
       else: return print("NO SOLUTION")
    else: return print("NO SOLUTION")
    return x
        
def scaling(a,n):
    s=[0]*n
    for i in range(0,n):
        s[i]=abs(a[i][0])
        for j in range(1,n):
            if abs(a[i][j]) > s[i] :
                s[i]=abs(a[i][j])
        if(s[i]==0):
            return -1
    return s

def pivot(a,b,s,n,k):
    p=k
    big=abs(Decimal(a[k][k])/Decimal(s[k]))
    for  i in range(k+1,n):
        temp=abs(Decimal(a[i][k])/Decimal(s[i]))
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
        steps.append([get_matrix(a,b),
                      "applying Pivoting ("+"R"+str(p+1)+"<->"+"R"+str(k+1)+")"])
def eliminate(a,b,s,n,tol):
    for k in range(0,n-1):
        pivot(a,b,s,n,k) #partial piovting
        if abs (Decimal(a[k][k])/Decimal(s[k])) < tol : #check singular
            return -1
        for i in range(k+1,n):
            factor =Decimal(a[i][k])/Decimal(a[k][k])
            for j in range(0,n):
                a[i][j]=Decimal(a[i][j])-(Decimal(factor)*Decimal(a[k][j]))
            b[i]=Decimal(b[i])-Decimal(factor)*Decimal(b[k])
            steps.append([get_matrix(a,b),
                      "Add("+"R"+str(i+1)+"+"+str(-float(factor))+"R"+str(k+1)+")"])

    if abs(a[n-1][n-1]/Decimal(s[n-1])) < tol :
        return -1

def substitute(a,b,n,x):
    x[n-1]=Decimal(b[n-1])/Decimal(a[n-1][n-1])
    steps.append([[],"value of x"+str(n)+"="+str(float(b[n-1]))+" / "+str(float(a[n-1][n-1]))+" = "+str(float(x[n-1]))])
    for i in range(n-2,-1,-1):
        sum=Decimal(0)
        for j in range(i+1,n):
            sum = sum+ Decimal(a[i][j])*Decimal(x[j])
        x[i]=(Decimal(b[i])-sum)/Decimal(a[i][i])
        steps.append([[],"value of x"+str(i+1)+"="+str(float(b[i]))+"-"+str(float(sum))+" / "+str(float(a[i][i]))+" = "+str(float(x[i]))])
        


matrix=[[0,2,3,10],[0,5,6,11],[1,1,1,12]]
x=gauss_elimination(matrix,3,5)
for step in steps:
    print(step[1])
    print_matrix(step[0])
print(x)