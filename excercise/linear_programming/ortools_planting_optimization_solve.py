import sys
import os
from ortools.linear_solver import pywraplp


def solve():
    filename = "planting_optimization_input.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = file.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    n = int(next(it))
    A = int(next(it))
    B = int(next(it))
    C = int(next(it))

    S = [int(next(it)) for _ in range(n)]
    W = [int(next(it)) for _ in range(n)]
    P = [int(next(it)) for _ in range(n)]

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Solver is not available...")
        sys.exit(0)

    X = [solver.NumVar(0, solver.infinity(), f"X[i]") for i in range(n)]

    area_constraint = solver.Constraint(0, A)
    seed_constraint = solver.Constraint(0, B)
    water_constraint = solver.Constraint(0, C)

    for i in range(n):
        area_constraint.SetCoefficient(X[i], 1)
        seed_constraint.SetCoefficient(X[i], S[i])
        water_constraint.SetCoefficient(X[i], W[i])

    obj = solver.Objective()
    for i in range(n):
        obj.SetCoefficient(X[i], P[i])
    obj.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(obj.Value())
        print(" ".join(str(X[i].solution_value()) for i in range(n)))

    else:
        print("NO OPTIMAL SOLUTION")


if __name__ == '__main__':
    solve()