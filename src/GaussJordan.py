from decimal import Decimal, getcontext

def get_matrix(matrix):
    return [[float(element) for element in row] for row in matrix]

#Gauss-Jordan elimination func
#arguments {augmented matrix, presicion}
#returns {values list, steps list}
def gauss_jordan_elimination(matrix, precision = 5):

    getcontext().prec = precision
    matrix = [[Decimal(element) for element in row] for row in matrix]
    dim = len(matrix)

    scaled_matrix = [row[:] for row in matrix]
    
    steps = []
    steps.append([get_matrix(matrix),"Original matrix"])

    #Scaling
    for i in range(dim):
        coef_max = max(abs(x) for x in matrix[i][:dim]) #maximum coeff in row
        for j in range(dim+1):
            scaled_matrix[i][j] /= coef_max
    
    steps.append([get_matrix(scaled_matrix),"Scaling the matrix"])
    #Solving
    for col in range(dim):
        #Pivoting
        indx_max = col #index of row with max value
        val_max = abs(scaled_matrix[col][col]) #maximum value in column
        for i in range(col+1,dim):
            val_tmp = abs(scaled_matrix[i][col])
            if val_tmp > val_max:
                val_max = val_tmp
                indx_max = i
        #Swap rows        
        if indx_max != col:
            matrix[col], matrix[indx_max] = matrix[indx_max], matrix[col]
            scaled_matrix[col], scaled_matrix[indx_max] = scaled_matrix[indx_max], scaled_matrix[col]
            steps.append([get_matrix(matrix),"applying Pivoting ("+"R"+str(col+1)+"<->"+"R"+str(indx_max+1)+")"])
        #Elimination
        pivot = matrix[col][col]
        if pivot != Decimal('0'):
            
            #divide row by pivot
            for j in range(col, dim+1):
                matrix[col][j] /= pivot 
            steps.append([get_matrix(matrix),"dividing R"+str(col+1)+" by "+str(pivot)])

            #subtract pivot row from other rows
            for i in range(dim):
                if i != col:
                    factor = matrix[i][col]
                    for j in range(col, dim+1):
                        matrix[i][j] -= factor * matrix[col][j]
            steps.append([get_matrix(matrix),"subtracting R"+str(col+1)+" from other rows"])
    
    #Solution
    values = []
    for row in matrix:
        values.append(float(row[-1]))
    return values, steps