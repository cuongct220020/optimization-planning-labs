import sys
import os
from ortools.linear_solver import pywraplp

def planting_opt_solver(n, seed_cost, water_cost, profit, seed_budget, water_budget, area_limit):

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("No solver available...")
        sys.exit(0)

    # Variables: area for each crop
    x = []
    for i in range(n):
        x.append(solver.NumVar(0, solver.infinity(), f"x_{i}"))

    # Constraints
    area_constraint = solver.Constraint(0, area_limit)
    seed_constraint = solver.Constraint(0, seed_budget)
    water_constraint = solver.Constraint(0, water_budget)

    for i in range(n):
        area_constraint.SetCoefficient(x[i], 1)
        seed_constraint.SetCoefficient(x[i], seed_cost[i])
        water_constraint.SetCoefficient(x[i], water_cost[i])

    # Objective: maximize profit
    objective = solver.Objective()
    for i in range(n):
        objective.SetCoefficient(x[i], profit[i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(objective.Value())
        print(" ".join(str(x[i].solution_value()) for i in range(n)))
    else:
        print("NOT_OPTIMAL")


if __name__ == '__main__':
    filename = "planting_optimization_input.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    # Input: n A B C
    n = int(next(it))
    A = float(next(it))   # area
    B = float(next(it))   # seed budget
    C = float(next(it))   # water budget

    seed_cost = [float(next(it)) for _ in range(n)]
    water_cost = [float(next(it)) for _ in range(n)]
    profit = [float(next(it)) for _ in range(n)]

    planting_opt_solver(n, seed_cost, water_cost, profit, B, C, A)