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
# precision   
def gauss_elimination(matrix,precision=5):
    
    matrix = [[Decimal(element) for element in row] for row in matrix]
    a = [row[:-1] for row in matrix] 
    b = [row[-1] for row in matrix]
    n=len(a)   
    getcontext().prec=precision
    
    steps.append([get_matrix(a,b),"Original matrix"])
    s=scaling(a,b,n)
    if s != -1 and s!=-2 :
       er=eliminate(a,b,s,n,tol=1e-12)
       if er != -1 and er!=-2:
          return substitute(a,b,n),steps
       elif er==-1 :raise ValueError("Infinite solutions")
       else: raise ValueError("NO solutions")
    elif s==-1 :raise ValueError("Infinite solutions")
    else: raise ValueError("NO solutions")
        
def scaling(a,b,n):
    s=[0]*n
    for i in range(0,n):
        s[i]=abs(a[i][0])
        for j in range(1,n):
            if abs(a[i][j]) > s[i] :
                s[i]=abs(a[i][j])
        if(s[i]== Decimal('0') ):
            if b[i] == Decimal('0'): return -1
            else: return -2 
    return s

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
        steps.append([get_matrix(a,b),
                      "applying Pivoting ("+"R"+str(p+1)+"<->"+"R"+str(k+1)+")"])
def eliminate(a,b,s,n,tol):
    for k in range(0,n-1):
        pivot(a,b,s,n,k) #partial piovting
        if abs ((a[k][k])/(s[k])) < tol : #check singular
            if b[k] == Decimal('0') : return -1
            else: return -2 
        for i in range(k+1,n):
            factor =(a[i][k])/(a[k][k])
            for j in range(0,n):
                a[i][j]=(a[i][j])-((factor)*(a[k][j]))
            b[i]=(b[i])-(factor)*(b[k])
            steps.append([get_matrix(a,b),
                      "Add("+"R"+str(i+1)+"+"+str(-float(factor))+"R"+str(k+1)+")"])

    if abs(a[n-1][n-1]/(s[n-1])) < tol :
        if b[n-1] == Decimal('0'): return -1
        else: return -2 

def substitute(a,b,n):
    x=[0]*n
    x[n-1]=(b[n-1])/(a[n-1][n-1])
    steps.append([[],"value of x"+str(n)+"="+str(float(b[n-1]))+" / "+str(float(a[n-1][n-1]))+" = "+str(float(x[n-1]))])
    for i in range(n-2,-1,-1):
        sum=(0)
        for j in range(i+1,n):
            sum = sum+ (a[i][j])*(x[j])
        x[i]=((b[i])-sum)/(a[i][i])
        steps.append([[],"value of x"+str(i+1)+"="+str(float(b[i]))+"-"+str(float(sum))+" / "+str(float(a[i][i]))+" = "+str(float(x[i]))])
    return x


