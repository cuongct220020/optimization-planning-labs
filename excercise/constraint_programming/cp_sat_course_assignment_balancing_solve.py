import sys
import os

from ortools.sat.python import cp_model


def cp_sat_solve(m, n, preferences, credit, conflicts):
    model = cp_model.CpModel()

    x = {}
    for t in range(m):
        pref = preferences[t]
        for i in pref:
            x[t, i] = model.NewBoolVar(f"x[{t}, {i}]")

    # Each course is assigned to exactly one teacher
    course_to_teachers = [[] for _ in range(n)]
    for (t, i), var in x.items():
        course_to_teachers[i].append(var)

    for i in range(n):
        model.Add(sum(course_to_teachers[i]) == 1)

    # Teacher cannot assign to course in conflicts
    for t in range(m):
        pref = preferences[t]
        pref_set = set(pref)
        for i in pref:
            for j in conflicts[i]:
                if j in pref_set and i < j:
                    model.Add(x[t, i] + x[t, j] <= 1)

    total_load = sum(credit)

    load = []
    for t in range(m):
        lt = model.NewIntVar(0, total_load, f"load[{t}]")
        model.Add(
            lt == sum(credit[i] * x[t, i] for i in preferences[t])
        )
        load.append(lt)

    lower_load = max(max(credit), total_load // m)
    upper_load = max(sum(credit[i] for i in preferences[t]) for t in range(m))
    max_load = model.NewIntVar(lower_load, upper_load, "max_load")

    for t in range(m):
        model.Add(max_load >= load[t])

    model.Minimize(max_load)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 0.95
    solver.parameters.num_search_workers = 8
    solver.parameters.log_search_progress = False


    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(solver.Value(max_load))

        # for t in range(m):
        #     course_assigned = []
        #     total_credit = 0
        #
        #     for i in preferences[t]:
        #         if solver.Value(x[t, i]) == 1:
        #             course_assigned.append(i + 1)
        #             total_credit += credit[i]
        #
        #     print(total_credit, " ".join(str(c) for c in course_assigned))
    else:
        print(-1)

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
    for _ in range(m):
        num_course = int(next(it))
        t = []
        for _ in range(num_course):
            t.append(int(next(it)) - 1)
        preferences.append(t)


    credit = []
    for _ in range(n):
        credit.append(int(next(it)))


    k = int(next(it))
    conflicts = [set() for _ in range(n)]
    for _ in range(k):
        i = int(next(it)) - 1
        j = int(next(it)) - 1
        conflicts[i].add(j)


    cp_sat_solve(m, n, preferences, credit, conflicts)