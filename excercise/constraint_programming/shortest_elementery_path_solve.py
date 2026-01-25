import sys
import os

from ortools.sat.python import cp_model

def shortest_elementery_path_solve(n, m, k, s, t, edges, forbidden_pairs):
    # Define CP model
    model = cp_model.CpModel()

    # Define decision variables
    x = {}
    for u, v, _ in edges:
        x[u, v] = model.NewIntVar(0, 1, f"x[{u}, {v}]")

    rank = {}
    for i in range(n):
        rank[i] = model.NewIntVar(0, n, f"rank[{i}]")

    # Define constraints
    # Tạo danh sách kề
    in_edges = {i: [] for i in range(n)}
    out_edges = {i: [] for i in range(n)}

    for u, v, _ in edges:
        out_edges[u].append(x[u, v])
        in_edges[v].append(x[u, v])

    for i in range(n):
        if i == s:
            model.Add(sum(out_edges[i]) == 1)
            model.Add(sum(in_edges[i]) == 0)
        elif i == t:
            model.Add(sum(in_edges[i]) == 1)
            model.Add(sum(out_edges[i]) == 0)
        else:
            sum_out = sum(out_edges[i])
            sum_in = sum(in_edges[i])
            model.Add(sum_out == sum_in)
            model.Add(sum_in <= 1)


    model.Add(rank[s] == 0)
    for u, v, _ in edges:
        model.Add(rank[v] == rank[u] + 1).OnlyEnforceIf(x[u, v])

    for u1, v1, u2, v2 in forbidden_pairs:
        model.Add(x[u1, v1] + x[u2, v2] <= 1)

    # Define Objective
    obj = 0
    for u, v, c in edges:
        obj += x[u, v] * c
    model.Minimize(obj)

    # Solving
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(int(solver.ObjectiveValue()))
    else:
        print("No solution")



if __name__ == "__main__":
    filename = "shortest_elementery_path_input.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = file.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    s = int(next(it))
    t = int(next(it))

    edges = []
    for i in range(m):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        edges.append((u, v, c))

    forbidden_pairs = []
    for i in range(k):
        u1 = int(next(it))
        v1 = int(next(it))
        u2 = int(next(it))
        v2 = int(next(it))
        forbidden_pairs.append((u1, v1, u2, v2))

    shortest_elementery_path_solve(n, m, k, s, t, edges, forbidden_pairs)