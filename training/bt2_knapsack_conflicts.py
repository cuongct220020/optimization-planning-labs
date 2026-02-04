import sys
import os

from ortools.linear_solver import pywraplp

if __name__ == '__main__':
    filename = "bt2_input.txt"
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))
    Q = int(next(it))

    w = [int(next(it)) for _ in range(n)]
    c = [int(next(it)) for _ in range(n)]

    m = int(next(it))
    conflicts = []
    for _ in range(m):
        i = int(next(it)) - 1
        j = int(next(it)) - 1
        conflicts.append((i, j))

    solver = pywraplp.Solver.CreateSolver("SCIP")

    x = [solver.BoolVar(f"x[{i}]") for i in range(n)]

    solver.Add(solver.Sum(x[i] * w[i] for i in range(n)) <= Q)

    for i, j in conflicts:
        solver.Add(x[i] + x[j] <= 1)

    obj = 0
    for i in range(n):
        obj += x[i] * c[i]
    solver.Maximize(obj)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        print(*(int(x[i].solution_value()) for i in range(n)))
    else:
        print("-1")