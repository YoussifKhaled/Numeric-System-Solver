import numpy as np
from CheloskyClass import CholeskySolver
from DoolitleClass import Doolitle
from GaussJordanClass import GaussJordanElimination
from GaussEliminationClass import GaussElimination
from JacobiClass import JacobiSolver
from GaussSeidelClass import GaussSeidelSolver
from CroutClass import CroutDecomposition
class LinearSolverEngine:
    def __init__(self, method, matrix, initial_guess=None, iterations=None, tol=None, precision=5,LU_Method="Doolitle"):
        self.method = method
        self.matrix = matrix
        self.initial_guess = initial_guess
        self.iterations = iterations
        self.tol = tol
        self.precision = precision
        self.LU_Method = LU_Method

    def solve(self):
        if self.method == 'Gauss-Jordan':
            solver = GaussJordanElimination(self.matrix, self.precision)
            return solver.gauss_jordan_elimination()
        elif self.method == 'Gauss Elimination':
            print("hnaa")
            solver = GaussElimination(self.matrix, self.precision)
            return solver.solve()
        elif self.method == 'Jacobi-Iteration':
            solver = JacobiSolver(self.matrix, self.initial_guess, self.iterations, self.tol, self.precision)
            return solver.jacobi()
        elif self.method == 'Gauss-Seidel':
            solver = GaussSeidelSolver(self.matrix, self.initial_guess, self.iterations, self.tol, self.precision)
            return solver.gauss_seidel()
        elif self.method == 'LU Decomposition':
            if self.LU_Method == "Doolitle":
                self.a, self.b = self.separate_augmented_matrix(self.matrix)
                solver = Doolitle(self.a, self.b ,self.precision, self.tol)
                solver.main()
                return solver.x, solver.steps
            elif self.LU_Method == "Cholesky":
                self.a, self.b = self.separate_augmented_matrix(self.matrix)
                solver = CholeskySolver(self.a,self.b,self.precision)
                solver.main()
                return solver.x, solver.steps
            elif self.LU_Method == "Crout":
                self.a, self.b = self.separate_augmented_matrix(self.matrix)
                solver = CroutDecomposition(self.a,self.b,self.precision)
                solver.crout()
                return solver.x, solver.steps

        else:
            raise ValueError("Invalid method. Supported methods: 'Gauss-Jordan', 'Gauss Elimination', 'Jacobi-Iteration,Gauss-Seidel'")


    def format_steps(self, steps):
        formatted_steps = ""
        if self.method == 'Jacobi-Iteration' or self.method == 'Gauss-Seidel' or self.method == 'LU Decomposition':
            for step in steps:
                formatted_steps += f"{step}\n"
            return formatted_steps

        for step in steps:
            formatted_steps += f"{step[1]}\n"
            for row in step[0]:
                formatted_steps += f"{row}\n"
        return formatted_steps


    def format_answer(self, ans, flag=True):
        
        if  flag and (ans == -1 or ans=="-1"):
            return "This system of equations will not converge"
        return f"Solution: {ans}"
    
    def separate_augmented_matrix(self,augmented_matrix):
        rows = len(augmented_matrix)

        if rows == 0:
            raise ValueError("Input matrix must have non-zero rows")

        cols_set = set(len(row) for row in augmented_matrix)
        if len(cols_set) != 1:
            raise ValueError("Invalid input matrix. Each row must have the same number of columns")

        num_cols_A = cols_set.pop() - 1

        A = np.array([row[:num_cols_A] for row in augmented_matrix])
        b = np.array([row[-1] for row in augmented_matrix])

        return A, b

# # Example usage
# A = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]

# # Gauss-Jordan Elimination
# engine = LinearSolverEngine(method='gauss_jordan', matrix=A)
# ans, steps = engine.solve()
# print("Gauss-Jordan Elimination:")
# formatted_answer = engine.format_answer(ans)
# print(formatted_answer)

# # Gauss Elimination
# engine = LinearSolverEngine(method='gauss_elimination', matrix=A)
# ans, steps = engine.solve()
# print("\nGauss Elimination:")
# formatted_answer = engine.format_answer(ans)
# print(formatted_answer)

# # Jacobi Iterative Solver
# A = [[1, 0, 0, 10], [1, 1, 0, 16], [0, 0, 1, 3]]
# engine = LinearSolverEngine(method='jacobi', matrix=A, initial_guess=[1, 1, 1], iterations=20, tol=0.001, precision=7)
# ans, steps = engine.solve()
# print("\nJacobi Iterative Solver:")
# formatted_answer = engine.format_answer(ans)
# print(formatted_answer)

# # Example usage
# A = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]

# # Gauss-Jordan Elimination
# engine = LinearSolverEngine(method='gauss_jordan', matrix=A)
# ans, steps = engine.solve()
# print("Gauss-Jordan Elimination:")
# print(ans)
# formatted_steps = engine.format_steps(steps)
# print(formatted_steps)

# # Gauss Elimination
# engine = LinearSolverEngine(method='gauss_elimination', matrix=A)
# ans, steps = engine.solve()
# print("\nGauss Elimination:")
# print(ans)
# formatted_steps = engine.format_steps(steps)
# print(formatted_steps)

# # Jacobi Iterative Solver
# A = [[1, 0, 0, 10], [1, 1, 0, 16], [0, 0, 1, 3]]
# engine = LinearSolverEngine(method='jacobi', matrix=A, initial_guess=[1, 1, 1], iterations=20, tol=0.001, precision=7)
# ans, steps = engine.solve()
# print("\nJacobi Iterative Solver:")
# print(ans)
# formatted_steps = engine.format_steps(steps)
# print(formatted_steps)

# Doolitle
# A = np.array([[1, 1, 2,8], [-1, -2, 3,1], [3, 7, 4,10]])
# engine = LinearSolverEngine(method='LU Decomposition', matrix=A, LU_Method="Doolitle")
# ans, steps = engine.solve()
# print("\nDoolitle:")
# print(ans)
# # for step in steps:
# #     print(step)
# formatted_steps = engine.format_steps(steps)
# print(formatted_steps)

# Crout
A = np.array([[1, 1, 2,8], [-1, -2, 3,1], [3, 7, 4,10]])
engine = LinearSolverEngine(method='LU Decomposition', matrix=A, LU_Method="Crout")
ans, steps = engine.solve()
print("\nCrout:")
print(ans)
# for step in steps:
#     print(step)
formatted_steps = engine.format_steps(steps)
print(formatted_steps)

    