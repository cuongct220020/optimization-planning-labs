import sys
import os

from ortools.linear_solver import pywraplp

def blood_type_correction_solve(n, individuals):
    # Tạo SCIP Solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print('No solver available...')
        sys.exit(0)

    # Mapping nhóm máu sang chỉ số: O=0, A=1, B=2, AB=3
    blood_types_mapping = {"O": 0, "A": 1, "B": 2, "AB": 3}
    blood_types = ["O", "A", "B", "AB"]

    # Mapping id to index
    id_to_idx = {ind[0]: i for i, ind in enumerate(individuals)}

    # x[i][j]: cá nhân i có nhóm máu j không (j: 0=O, 1=A, 2=B, 3=AB)
    x = {}
    for i in range(n):
        for j in range(4):
            x[i, j] = solver.BoolVar(f"x[{i}, {j}]")

    # y[i]: cá nhân i có thay đổi nhóm máu không
    y = {}
    for i in range(n):
        y[i] = solver.BoolVar(f"y[{i}]")

    # z cho cặp cha-mẹ (để xử lý trường hợp A+B hoặc B+A)
    couples = set()
    for i in range(n):
        _, _, f_id, m_id = individuals[i]
        if f_id != -1 and m_id != -1:
            f_idx = id_to_idx[f_id]
            m_idx = id_to_idx[m_id]
            couples.add((f_idx, m_idx))

    z = {}
    for f_idx, m_idx in couples:
        z[f_idx, m_idx] = solver.BoolVar(f"z[{f_idx}, {m_idx}]")
        z[m_idx, f_idx] = solver.BoolVar(f"z[{m_idx}, {f_idx}]")

    # Constraint 5: Mỗi cá nhân chỉ có đúng 1 nhóm máu
    for i in range(n):
        solver.Add(sum(x[i, j] for j in range(4)) == 1)

    # Constraints 1 - 4: Nếu không thay đổi (y[i]=0), giữ nguyên nhóm máu ban đầu
    for i in range(n):
        _, blood_type, _, _ = individuals[i]
        bt_idx = blood_types_mapping[blood_type]
        solver.Add(x[i, bt_idx] >= 1 - y[i])

    # Constraints 16 -19: Nếu thay đổi nhóm máu thì y[i] = 1
    for i in range(n):
        _, blood_type, _, _ = individuals[i]
        bt_idx = blood_types_mapping[blood_type]
        for j in range(4):
            if j != bt_idx:
                solver.Add(y[i] >= x[i, j])

    # Constraints 6 - 11: Định nghĩa biến z
    # z[f_idx, m_idx] = 1 nếu bố là A (x[f_idx, 1] = 1), mẹ là B (x[m_idx, 2] = 1)
    for f_idx, m_idx in couples:
        solver.Add(z[f_idx, m_idx] <= x[f_idx, 1])
        solver.Add(z[f_idx, m_idx] <= x[m_idx, 2])
        solver.Add(x[f_idx, 1] + x[m_idx, 2] <= z[f_idx, m_idx] + 1)

        solver.Add(z[m_idx, f_idx] <= x[m_idx, 1])
        solver.Add(z[m_idx, f_idx] <= x[f_idx, 2])
        solver.Add(x[m_idx, 1] + x[f_idx, 2] <= z[m_idx, f_idx] + 1)


    # Constraint 12 - 15: Ràng buộc cho các quy tắc di truyền nhóm máu
    for i in range(n):
        _, _, f_id, m_id = individuals[i]

        if f_id != -1 and m_id != -1:
            f_idx = id_to_idx[f_id]
            m_idx = id_to_idx[m_id]

            # Rule 12: Nếu con thuộc nhóm máu O thì cả cha, mẹ không thuộc nhóm máu AB
            solver.Add(2 * (1 - x[i, 0]) - x[f_idx, 3] - x[m_idx, 3] >= 0)

            # Rule 13: Nếu con thuộc nhóm máu A thì ít nhất cha, hoặc mẹ thuộc nhóm máu A, hoặc AB
            solver.Add((1 - x[i, 1]) + x[f_idx, 1] + x[m_idx, 1] + x[f_idx, 3] + x[m_idx, 3] >= 1)

            # Rule 14: Nếu con thuộc nhóm máu B thì ít nhất cha, hoặc mẹ thuộc nhóm máu B, hoặc AB
            solver.Add((1 - x[i, 2]) + x[f_idx, 2] + x[m_idx, 2] + x[f_idx, 3] + x[m_idx, 3] >= 1)

            # Rule 15: Nếu con thuộc nhóm máu AB thì chia thành 3 trường hợp:
            # TH1: Ít nhất bố hoặc mẹ thuộc nhóm máu AB
            # TH2: Cả bố và mẹ không thuộc nhóm máu O
            # TH3: Bố thuộc nhóm máu A, mẹ thuộc nhóm máu B và ngược lại
            solver.Add((1 - x[i, 3]) + x[m_idx, 3] + x[f_idx, 3] - (x[m_idx, 0] + x[f_idx, 0]) + z[m_idx, f_idx] + z[f_idx, m_idx] >= 1)

    obj = solver.Objective()
    for i in range(n):
        obj.SetCoefficient(y[i], 1)
    obj.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(obj.Value()))
    else:
        print('No solution found')

if __name__ == '__main__':
    filename = "ip_blood_type_correction_input.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    n = int(next(it))

    individuals = []
    for _ in range(n):
        id = int(next(it))
        blood_type = str(next(it))
        father_id = int(next(it))
        mother_id = int(next(it))
        individuals.append((id, blood_type, father_id, mother_id))

    blood_type_correction_solve(n, individuals)
