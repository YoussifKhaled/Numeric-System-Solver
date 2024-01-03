
from sympy import Symbol, sympify
from sympy import Symbol, diff
from sympy import Symbol, lambdify
from sympy.plotting import plot

from sympy import symbols
from decimal import Decimal, getcontext
import re


def newton(x,fx,f1x,tol,iter,x0):

    Steps = []

    for i in range(1,iter+1):
        fxi = Decimal(str(fx.subs(x,x0).evalf(n=getcontext().prec)))
        f1xi = Decimal(str(f1x.subs(x,x0).evalf(n=getcontext().prec)))
        
        if(abs(f1xi) < 1e-12):
            break
        
        x1 = Decimal(x0) - fxi / f1xi

        if(float(x1) == 0):
            error = Decimal(abs((float(x1) - x0)*100/(float(x1)+1)))+Decimal('0')
        else:
            error = Decimal(abs((float(x1) - x0)*100/float(x1)))+Decimal('0')

        Steps.append('Iteration'+ str(i) +': xi='+str(x0)+' f(xi)='+str(fxi)+' f\'(xi)='+str(f1xi) + ' xi+1='+str(x1) + ' εi='+str(error)+'%')
        
        if float(error) < tol:
            break
        
        x0 = float(x1)
    return x0,Steps

def modified_newton1(x,fx,f1x,tol,iter,x0,m):
    
    Steps = []

    for i in range(1,iter+1):
        fxi = Decimal(str(fx.subs(x,x0).evalf(n=getcontext().prec)))
        f1xi = Decimal(str(f1x.subs(x,x0).evalf(n=getcontext().prec)))
        
        if(abs(f1xi) < 1e-12):
            break
        
        x1 = Decimal(x0) - m * (fxi / f1xi)

        if(float(x1) == 0):
            error = Decimal(abs((float(x1) - x0)*100/(float(x1)+1)))+Decimal('0')
        else:
            error = Decimal(abs((float(x1) - x0)*100/float(x1)))+Decimal('0')

        Steps.append('Iteration'+ str(i) +': xi='+str(x0)+' f(xi)='+str(fxi)+' f\'(xi)='+str(f1xi) + ' xi+1='+str(x1) + ' εi='+str(error)+'%')
        
        if float(error) < tol:
            break
        
        x0 = float(x1)
    return x0,Steps

def modified_newton2(x,fx,f1x,f2x,tol,iter,x0):

    Steps = []

    for i in range(1,iter+1):
        fxi = Decimal(str(fx.subs(x,x0).evalf(n=getcontext().prec)))
        f1xi = Decimal(str(f1x.subs(x,x0).evalf(n=getcontext().prec)))
        f2xi = Decimal(str(f2x.subs(x,x0).evalf(n=getcontext().prec)))
        
        if(abs(f1xi**2 - (fxi * f2xi)) < 1e-12):
            break
        
        x1 = Decimal(x0) - (fxi * f1xi)/(f1xi ** 2 - fxi * f2xi)
        
        if(float(x1) == 0):
            error = Decimal(abs((float(x1) - x0)*100/(float(x1)+1)))+Decimal('0')
        else:
            error = Decimal(abs((float(x1) - x0)*100/float(x1)))+Decimal('0')
        
        Steps.append('Iteration'+ str(i) +': xi='+str(x0)+' f(xi)='+str(fxi)+' f\'(xi)='+str(f1xi) + ' f\'\'(xi)='+str(f2xi) + ' xi+1='+str(x1) + ' εi='+str(error)+'%')
        
        if float(error) < tol:
            break
        
        x0 = float(x1)
    return x0,Steps

def chef(Operation, Expression, x0,tol=1e-5, iter=50, precision=5, m=1):
    getcontext().prec = precision
    getcontext().rounding = 'ROUND_HALF_UP'

    Expression = Expression.replace('^', '**').lower().replace('e', 'E').replace(' ', '')
    Expression = re.sub(r'(\d+)x', r'\1*x', Expression)

    try:
        x = Symbol('x')
        fx = sympify(Expression)
        f1x = diff(fx)
        f2x = diff(f1x)
        #------plot----
        min_x = -10   # you can take it as input 
        max_x = 10
        p = plot(fx, (x, min_x, max_x), show=False)
        p.title = fx
        p.ylabel = ''
        p.xlabel = ''
        p.show()
    except:
        return 'Invalid Expression',[]
    
    
    Xroot = None
    Steps = None

    if Operation == 'Newton':
        Xroot,Steps = newton(x,fx,f1x,tol,iter,x0)
    elif Operation == 'Modified Newton1':
        Xroot,Steps = modified_newton1(x,fx,f1x,tol,iter,x0,m)
    else: #Operation == 'Modified Newton2'
        Xroot,Steps = modified_newton2(x,fx,f1x,f2x,tol,iter,x0)

    return Xroot,Steps

def main():
   
    Expression = 'X**3-2*x^2-4*x+8'
    m = 3
    x0= 4
    print('Expression: '+Expression)
    print('Newton method:')
    xroot,stps = chef('Newton',Expression,x0,1e-4,100,5)
    print('Root = '+str(xroot))
    for stp in stps:
        print(stp)
    print('---------------------------------------------')
    print('Modified1 Newton method:')
    xroot,stps = chef('Modified Newton1',Expression,x0,1e-4,100,5,m)
    print('Root = '+str(xroot))
    for stp in stps:
        print(stp)
    print('---------------------------------------------')
    print('Modified2 Newton method:')
    xroot,stps = chef('Modified Newton2',Expression,x0,1e-4,100,5)
    print('Root = '+str(xroot))
    for stp in stps:
        print(stp)

if __name__ == '__main__':
    main()