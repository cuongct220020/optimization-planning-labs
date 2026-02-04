import sys
import os
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_tsp(dist_matrix, n):
    # 1. Tạo Routing Index Manager
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    # n nodes, 1 vehicle, start node = 0

    # 2. Tạo Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # 3. Callback trả về chi phí đi từ i -> j
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return dist_matrix[from_node][to_node]

    cb = routing.RegisterTransitCallback(distance_callback)

    # 4. Gán hàm chi phí cho tất cả xe
    routing.SetArcCostEvaluatorOfAllVehicles(cb)

    # 5. Cấu hình chiến lược tìm lời giải
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Local search để cải thiện nghiệm
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = 5   # có thể tăng nếu muốn tốt hơn

    # 6. Giải
    solution = routing.SolveWithParameters(search_parameters)

    if solution is None:
        return []

    # 7. Truy vết tour
    route = []
    index = routing.Start(0)

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(node + 1)   # +1 vì đề bài đánh số từ 1
        index = solution.Value(routing.NextVar(index))

    return route


if __name__ == '__main__':
    filename = "tsp_input.txt"

    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))

    # Đọc ma trận khoảng cách
    dist_matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = int(next(it))

    route = solve_tsp(dist_matrix, n)

    # Output
    print(n)
    print(" ".join(map(str, route)))