import sys
import os

from ortools.linear_solver import pywraplp

if __name__ == '__main__':
    filename = "course_assignment_balancing_input.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = file.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    m = int(next(it))
    n = int(next(it))

    preferences = []
    for t in range(m):
        num_pref_courses = int(next(it))
        t = []
        for i in range(num_pref_courses):
            t.append(int(next(it)) - 1)
        preferences.append(t)

    credits = []
    for _ in range(n):
        credits.append(int(next(it)))

    k = int(next(it))
    conflicts = [set() for _ in range(n)]
    for _ in range(k):
        i = int(next(it)) - 1
        j = int(next(it)) - 1
        conflicts[i].add(j)

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        print("solver is not available...")
        sys.exit(0)

    # Define variables
    x = {}
    for t in range(m):
        for i in preferences[t]:
            x[t, i] = solver.BoolVar(f"x[{t}, {i}]")

    load = []
    for t in range(m):
        lt = solver.IntVar(0, solver.infinity(), f"load[{t}]")
        load.append(lt)

    for t in range(m):
        solver.Add(sum(credits[i] * x[t, i] for i in preferences[t]) <= load[t])

    lower = max(max(credits), sum(credits) // m)
    upper = max(sum(credits[i] for i in preferences[t]) for t in range(m))
    max_load = solver.IntVar(lower, upper, "max_load")

    for t in range(m):
        solver.Add(max_load >= load[t])


    # Define constraints
    for t in range(m):
        pref_list = preferences[t]
        pref_set = set(pref_list)
        for i in pref_list:
            for j in conflicts[i]:
                if j in pref_set and i < j:
                    solver.Add(x[t, i] + x[t, j] <= 1)

    course_to_teachers = [set() for _ in range(n)]
    for (t, i), var in x.items():
        course_to_teachers[i].add(var)

    for i in range(n):
        solver.Add(sum(course_to_teachers[i]) == 1)


    # Define objective
    obj = solver.Minimize(max_load)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(max_load.solution_value()))

    else:
        print("-1")