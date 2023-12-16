from decimal import Decimal, getcontext

#Gets matrix values as float
def get_matrix(matrix):
    return [[float(element) for element in row] for row in matrix]

#Gauss-Jordan elimination func
#arguments {augmented matrix, presicion}
#returns {values list, steps list}
def gauss_jordan_elimination(matrix, precision = 5):

    getcontext().prec = precision
    matrix = [[Decimal(element) for element in row] for row in matrix] #Converting to decimal
    dim = len(matrix)

    scaled_matrix = [row[:] for row in matrix]
    
    steps = []
    steps.append([get_matrix(matrix),"Original matrix"])

    #Scaling
    for row in range(dim):
        coef_max = max(abs(x) for x in matrix[row][:dim]) #maximum coeff in row
        if coef_max == Decimal('0'):
            if matrix[row][dim] != Decimal('0'):
                raise ValueError("Matrix is inconsistent,No solution")
            else:
                raise ValueError("Infinite solutions")
        for col in range(dim+1):
            scaled_matrix[row][col] /= coef_max
    steps.append([get_matrix(scaled_matrix),"Scaling the matrix"])
    
    #Solving
    for row in range(dim):

        #Pivoting
        indx_max = row #index of row with max value
        val_max = abs(scaled_matrix[row][row]) #Value of current pivot
        for i in range(row+1,dim): #searching for max element below pivot to swap with pivot
            val_tmp = abs(scaled_matrix[i][row])
            if val_tmp > val_max:
                val_max = val_tmp
                indx_max = i
        
        #Swap rows        
        if indx_max != row:
            matrix[row], matrix[indx_max] = matrix[indx_max], matrix[row]
            scaled_matrix[row], scaled_matrix[indx_max] = scaled_matrix[indx_max], scaled_matrix[row]
            steps.append([get_matrix(matrix),"applying Pivoting ("+"R"+str(row+1)+"<->"+"R"+str(indx_max+1)+")"])
        
        pivot = matrix[row][row]
        #divide row by pivot
        if pivot != Decimal('0'):
            for j in range(row, dim+1):
                matrix[row][j] /= pivot 
            steps.append([get_matrix(matrix),"dividing R"+str(row+1)+" by "+str(pivot)])

        #subtract scaled pivot row from other rows
        for i in range(dim):
            if i != row:
                factor = matrix[i][row]
                for j in range(row, dim+1):
                    matrix[i][j] -= factor * matrix[row][j]
                val_max_check = max(abs(x) for x in matrix[i][:dim])
                if val_max_check == Decimal('0'):
                    if matrix[i][dim] != Decimal('0'):
                        raise ValueError("Matrix is inconsistent,No solution")
                    else:
                        raise ValueError("Infinite solutions")
                if factor == Decimal('0'):
                    continue
                steps.append([get_matrix(matrix),"Adding ("+str(-factor)+")*R"+str(row+1)+" to R"+str(i+1)])

    #Solution
    values = []
    for row in matrix:
        values.append(float(row[-1]))

    return values, steps