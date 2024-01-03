from sympy import Symbol, sympify
from sympy import Symbol, diff
from sympy import re as real
from decimal import Decimal, getcontext
import re
import math

def newton(x,fx,f1x,tol,iter,x0):

    Steps = []
    for i in range(1,iter+1):
        fxi = Decimal(str(real(fx.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore
        f1xi = Decimal(str(real(f1x.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore
        
        if(abs(f1xi) < 1e-12):
            Steps.append('Derivative is zero,So method fails')
            break
        
        x1 = Decimal(x0) - fxi / f1xi

        if(float(x1) == 0):
            error = Decimal(abs((float(x1) - x0)*100/(float(x1)+1)))+Decimal('0')
        else:
            error = Decimal(abs((float(x1) - x0)*100/float(x1)))+Decimal('0')

        Steps.append('Iteration'+ str(i) +': xi='+str(x0)+' f(xi)='+str(fxi)+' f\'(xi)='+str(f1xi) + ' xi+1='+str(x1) + ' εi='+str(error)+'%')
        
        if float(error) < tol:
            Steps.append('Relative error < tolerance, So method converges')
            break
        if(i == iter): 
          Steps.append('Not convergent in given maximum step count.')
        x0 = float(x1)
    return x0,Steps

def modified_newton1(x,fx,f1x,tol,iter,x0,m):
    
    Steps = []

    for i in range(1,iter+1):
        fxi = Decimal(str(real(fx.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore
        f1xi = Decimal(str(real(f1x.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore
        
        if(abs(f1xi) < 1e-12):
            Steps.append('Derivative is zero,So method fails')
            break
        
        x1 = Decimal(x0) - m * (fxi / f1xi)

        if(float(x1) == 0):
            error = Decimal(abs((float(x1) - x0)*100/(float(x1)+1)))+Decimal('0')
        else:
            error = Decimal(abs((float(x1) - x0)*100/float(x1)))+Decimal('0')

        Steps.append('Iteration'+ str(i) +': xi='+str(x0)+' f(xi)='+str(fxi)+' f\'(xi)='+str(f1xi) + ' xi+1='+str(x1) + ' εi='+str(error)+'%')
        
        if float(error) < tol:
            Steps.append('Relative error < tolerance, So method converges')
            break
        if(i == iter): 
          Steps.append('Not convergent in given maximum step count.')
        x0 = float(x1)
    return x0,Steps

def modified_newton2(x,fx,f1x,f2x,tol,iter,x0):

    Steps = []

    for i in range(1,iter+1):
        fxi = Decimal(str(real(fx.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore
        f1xi = Decimal(str(real(f1x.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore
        f2xi = Decimal(str(real(f2x.subs(x,x0).evalf(n=getcontext().prec)))) # type: ignore

        if math.isnan(fxi) or math.isnan(f1xi) or math.isnan(f2xi):
            Steps.append('Method Terminated')
            break
        if(abs(f1xi**2 - (fxi * f2xi)) < 1e-12):
            Steps.append('Divison by Zero ,So method fails')
            break
        
        x1 = Decimal(x0) - (fxi * f1xi)/(f1xi ** 2 - fxi * f2xi)
        
        if(float(x1) == 0):
            error = Decimal(abs((float(x1) - x0)*100/(float(x1)+1)))+Decimal('0')
        else:
            error = Decimal(abs((float(x1) - x0)*100/float(x1)))+Decimal('0')
        
        Steps.append('Iteration'+ str(i) +': xi='+str(x0)+' f(xi)='+str(fxi)+' f\'(xi)='+str(f1xi) + ' f\'\'(xi)='+str(f2xi) + ' xi+1='+str(x1) + ' εi='+str(error)+'%')
        
        if float(error) < tol:
            Steps.append('Relative error < tolerance, So method converges')
            break
        if(i == iter): 
          Steps.append('Not convergent in given maximum step count.')
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
   
    Expression = '(x-1)**(3)+0.512'
    #Expression = 'e**(-x)-x'
    m = 1
    x0= 2.5
    print('Expression: '+Expression)
    print('Newton method:')
    xroot,stps = chef('Newton',Expression,x0,1e-4,50,5)
    print('Root = '+str(xroot))
    for stp in stps:
        print(stp)
    print('---------------------------------------------')
    print('Modified1 Newton method:')
    xroot,stps = chef('Modified Newton1',Expression,x0,1e-4,50,5,m)
    print('Root = '+str(xroot))
    for stp in stps:
        print(stp)
    print('---------------------------------------------')
    print('Modified2 Newton method:')
    xroot,stps = chef('Modified Newton2',Expression,x0,1e-4,50,5)
    print('Root = '+str(xroot))
    for stp in stps:
        print(stp)

if __name__ == '__main__':
    main()
