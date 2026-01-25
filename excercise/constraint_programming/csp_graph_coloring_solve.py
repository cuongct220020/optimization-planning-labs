import sys
import os

from ortools.sat.python import cp_model

def csp_graph_coloring_solve(n, edges):
    model = cp_model.CpModel()

    color = {}
    for i in range(1, n + 1):
        color[i] = model.NewIntVar(1, n, f"color[{i}]")

    num_colors = model.NewIntVar(1, n, "num_colors")

    for u, v in edges:
        model.Add(color[u] != color[v])

    model.AddMaxEquality(num_colors, [color[i] for i in range(1, n + 1)])

    model.Minimize(num_colors)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result_colors = [solver.Value(color[i]) for i in range(1, n + 1)]
        num_used_colors = solver.Value(num_colors)
        return result_colors, num_used_colors
    else:
        return None, None


if __name__ == '__main__':
    filename = "graph_coloring_input.txt"

    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        edges.append((u, v))

    result_colors, num_used_colors = csp_graph_coloring_solve(n, edges)
    if result_colors:
        print(num_used_colors)
        print(" ".join(map(str, result_colors)))
    else:
        print("No solution found!")
