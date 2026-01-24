import sys
import os

from ortools.linear_solver import pywraplp

n = -1
c = []
sec_list = []


def milp_solve():
    global n, c, sec_list

    solver = pywraplp.Solver.CreateSolver("SCIP")

    # Define variables
    x = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(solver.IntVar(0, 1, f"x[{i}][{j}]"))
        x.append(row)

    # Define objective
    obj = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                obj += c[i][j] * x[i][j]

    solver.Minimize(obj)

    # Define Constraint
    for i in range(n):
        go_in = 0
        go_out = 0
        for j in range(n):
            go_in += x[i][j]
            go_out += x[j][i]

        solver.Add(go_in == go_out)
        solver.Add(go_in == 1)
        solver.Add(x[i][i] == 0)

    for sec in sec_list:
        num_e = 0
        num_v = len(sec)
        for i in range(num_v):
            u = sec[i]
            for j in range(i + 1, num_v):
                v = sec[j]
                num_e += x[u][v] + x[v][u]

        solver.Add(num_e <= num_v - 1)

    # Solving
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:

        # Check subtour in relaxation problem
        next_node = [-1] * n
        for i in range(n):
            for j in range(n):
                if int(x[i][j].solution_value()) > 0:
                    next_node[i] = j
                    # print(f"{i} => {j}")
                    break

        mark = [False] * n
        new_sec_list = []

        for i in range(n):
            if not mark[i]:
                curr = i
                sec = []
                while not mark[curr]:
                    sec.append(curr)
                    mark[curr] = True
                    curr = next_node[curr]
                new_sec_list.append(sec)

        if len(new_sec_list) > 1:
            for sec in new_sec_list:
                if len(sec) < n:
                    sec_list.append(sec)
            return None
        else:
            return solver.Objective().Value()

    else:
        return None

if __name__ == '__main__':
    filename = "ip_tsp_input.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))

    for _ in range(n):
        row = []
        for _ in range(n):
            row.append(int(next(it)))
        c.append(row)

    while True:
        result = milp_solve()

        if result is not None:
            print(int(result))
            break
        # else:
        #     print(-1)