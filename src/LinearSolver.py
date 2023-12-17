from GaussJordanClass import GaussJordanElimination
from GaussEliminationClass import GaussElimination
from JacobiClass import JacobiSolver
class LinearSolverEngine:
    def __init__(self, method, matrix, initial_guess=None, iterations=None, tol=None, precision=5):
        self.method = method
        self.matrix = matrix
        self.initial_guess = initial_guess
        self.iterations = iterations
        self.tol = tol
        self.precision = precision

    def solve(self):
        if self.method == 'Gauss-Jordan':
            solver = GaussJordanElimination(self.matrix, self.precision)
            return solver.solve()
        elif self.method == 'Gauss Elimination':
            print("hnaa")
            solver = GaussElimination(self.matrix, self.precision)
            return solver.solve()
        elif self.method == 'Jacobi-Iteration':
            solver = JacobiSolver(self.matrix, self.initial_guess, self.iterations, self.tol, self.precision)
            return solver.jacobi()
        else:
            raise ValueError("Invalid method. Supported methods: 'Gauss-Jordan', 'Gauss Elimination', 'Jacobi-Iteration'")


    def format_steps(self, steps):
        formatted_steps = ""
        if self.method == 'Jacobi-Iteration':
            for step in steps:
                formatted_steps += f"{step}\n"
            return formatted_steps

        for step in steps:
            formatted_steps += f"{step[1]}\n"
            for row in step[0]:
                formatted_steps += f"{row}\n"
        return formatted_steps


    def format_answer(self, ans):
        return f"Solution: {ans}"

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
