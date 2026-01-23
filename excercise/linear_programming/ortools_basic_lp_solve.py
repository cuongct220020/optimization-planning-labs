"""
Linear Programming Solver using OR-Tools

Problem Description:
-------------------
Solve the linear programming problem:
    Maximize: f(x) = C[1]*X[1] + C[2]*X[2] + ... + C[n]*X[n]

Subject to constraints:
    low[1] <= A[1,1]*X[1] + A[1,2]*X[2] + ... + A[1,n]*X[n] <= up[1]
    low[2] <= A[2,1]*X[1] + A[2,2]*X[2] + ... + A[2,n]*X[n] <= up[2]
    ...
    low[m] <= A[m,1]*X[1] + A[m,2]*X[2] + ... + A[m,n]*X[n] <= up[m]

Variable bounds:
    DL[i] <= X[i] <= DU[i], for i = 1, 2, ..., n

Input Format:
------------
Line 1: Two positive integers n and m (1 <= n, m <= 1000)
        - n: number of variables
        - m: number of constraints

Lines 2 to n+1: For each variable i, two integers DL[i] and DU[i]
        - DL[i]: lower bound of variable X[i]
        - DU[i]: upper bound of variable X[i]

Line n+2: n integers C[1], C[2], ..., C[n]
        - C[i]: coefficient of variable X[i] in the objective function

Lines n+3 to n+m+2: For each constraint i, n integers A[i,1], A[i,2], ..., A[i,n]
        - A[i,j]: coefficient of variable X[j] in constraint i

Lines n+m+3 to n+2m+2: For each constraint i, two integers low[i] and up[i]
        - low[i]: lower bound of constraint i
        - up[i]: upper bound of constraint i

Output Format:
-------------
If the problem has an optimal solution:
    Line 1: n (number of variables)
    Line 2: X[1] X[2] ... X[n] (optimal values separated by spaces)

If the problem does not have an optimal solution:
    Print "NOT_OPTIMAL"

Example:
--------
Input:
3 3
2 100000
2 100000
0 10
2 4 -1
4 -1 2
1 1 1
3 1 -2
-100000 7
5 5
-100000 10

This represents:
- 3 variables, 3 constraints
- Variable bounds: 2 <= X[1] <= 100000, 2 <= X[2] <= 100000, 0 <= X[3] <= 10
- Objective: Maximize 2*X[1] + 4*X[2] - 1*X[3]
- Constraints:
    3 <= 4*X[1] - 1*X[2] + 2*X[3] <= 1 (intentionally infeasible bound)
    5 <= 1*X[1] + 1*X[2] + 1*X[3] <= 5
    -100000 <= -2*X[1] <= 10
"""

import sys
import os


def lp_solver(n, m, dl, du, c, a, low, up):
    from ortools.linear_solver import pywraplp
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("No solver available...")
        sys.exit(0)

    x = []
    for i in range(n):
        var = solver.NumVar(dl[i], du[i], f"x_{i}")
        x.append(var)

    for i in range(m):
        constraint = solver.Constraint(low[i], up[i])

        for j in range(n):
            if a[i][j] != 0:
                constraint.SetCoefficient(x[j], a[i][j])

    objective = solver.Objective()
    for j in range(n):
        objective.SetCoefficient(x[j], c[j])

    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        print(" ".join([str(x[i].solution_value()) for i in range(n)]))
    else:
        print("NOT_OPTIMAL")


if __name__ == '__main__':
    # Step 1: Read Console Input
    filename = "basic_lp_input.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    dl, du = [], []
    for _ in range(n):
        dl.append(int(next(it)))
        du.append(int(next(it)))

    c = []
    for _ in range(n):
        c.append(int(next(it)))

    a = []
    for _ in range(m):
        row = [int(next(it)) for _ in range(n)]
        a.append(row)

    low, up = [], []
    for _ in range(m):
        low.append(int(next(it)))
        up.append(int(next(it)))

    # Step 2: LP Solving
    lp_solver(n, m, dl, du, c, a, low, up)


import sys
import os

def lp_solver(n, m, dl, du, c, a, low, up):
    from ortools.linear_solver import pywraplp
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("No solver available...")
        sys.exit(0)

    x = []
    for i in range(n):
        var = solver.NumVar(dl[i], du[i], f"x_{i}")
        x.append(var)

    for i in range(m):
        constraint = solver.Constraint(low[i], up[i])

        for j in range(n):
            if a[i][j] != 0:
                constraint.SetCoefficient(x[j], a[i][j])


    objective = solver.Objective()
    for j in range(n):
        objective.SetCoefficient(x[j], c[j])

    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        print(" ".join([str(x[i].solution_value()) for i in range(n)]))
    else:
        print("NOT_OPTIMAL")


if __name__ == '__main__':
    # Step 1: Read Console Input
    filename = "basic_lp_input.txt"

    if os.path.exists("basic_lp_input.txt"):
        with open("basic_lp_input.txt", "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    dl, du = [], []
    for _ in range(n):
        dl.append(int(next(it)))
        du.append(int(next(it)))

    c = []
    for _ in range(n):
        c.append(int(next(it)))

    a = []
    for _ in range(m):
        row = [int(next(it)) for _ in range(n)]
        a.append(row)

    low, up = [], []
    for _ in range(m):
        low.append(int(next(it)))
        up.append(int(next(it)))

    # Step 2: LP Solving
    lp_solver(n, m, dl, du, c, a, low, up)