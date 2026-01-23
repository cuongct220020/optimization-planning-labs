import sys
import os

from ortools.linear_solver import pywraplp


def solve():
    file = "simplex_method_input.txt"
    if os.path.exists(file):
        with open(file, "r") as file:
            data = file.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    C = [float(next(it)) for _ in range(n)]

    A = [[float(next(it)) for _ in range(n)] for _ in range(m)]

    b = [float(next(it)) for _ in range(m)]

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("UNBOUNDED")
        return

    # Variables: X[i] >= 0
    X = [solver.NumVar(0.0, solver.infinity(), f"x{i}") for i in range(n)]

    # Constraints: A x <= b
    for j in range(m):
        ct = solver.Constraint(-solver.infinity(), b[j])
        for i in range(n):
            ct.SetCoefficient(X[i], A[j][i])

    # Objective: maximize C^T x
    obj = solver.Objective()
    for i in range(n):
        obj.SetCoefficient(X[i], C[i])
    obj.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        print(" ".join(f"{X[i].solution_value():.6f}" for i in range(n)))
    else:
        print("UNBOUNDED")


if __name__ == "__main__":
    solve()