import sys
import os

from ortools.linear_solver import pywraplp

if __name__ == '__main__':
    filename = "bt1_input.txt"
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    A = int(next(it))
    n = int(next(it))
    m = int(next(it))

    types = []
    for _ in range(n):
        types.append(int(next(it)) - 1)

    a = []
    for _ in range(n):
        a.append(int(next(it)))

    b = []
    for _ in range(n):
        b.append(int(next(it)))

    c = []
    for _ in range(n):
        c.append(int(next(it)))

    d = []
    for _ in range(m):
        d.append(int(next(it)))

    solver = pywraplp.Solver.CreateSolver("GLOP")

    x = [solver.NumVar(0, c[i], f"x[{i}]") for i in range(n)]

    solver.Add(solver.Sum(x) <= A)

    for j in range(m):
        filtered_var = [x[i] for i in range(n) if type[i] == j]
        if filtered_var:
            solver.Add(solver.Sum(filtered_var) <= d[j])

    objective = 0
    for i in range(n):
        objective += x[i] * (b[i] - a[i])
    solver.Maximize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(f"{round(solver.Objective().Value()):.0f}")
    else:
        print("-1")