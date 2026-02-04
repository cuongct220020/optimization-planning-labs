import sys
import os
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve():
    data = sys.stdin.read().strip().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    up = int(next(it))
    uc = int(next(it))

    capacities = [int(next(it)) for _ in range(m)]

    demands = [0] * (n + 1)
    for i in range(1, n + 1):
        demands[i] = int(next(it))

    distance_matrix = []
    for _ in range(n + 1):
        row = []
        for _ in range(n + 1):
            row.append(int(next(it)))
        distance_matrix.append(row)

    manager = pywrapcp.RoutingIndexManager(n + 1, m, 0)
    routing = pywrapcp.RoutingModel(manager)

    # -------- distance cost --------
    def distance_callback(from_index, to_index):
        u = manager.IndexToNode(from_index)
        v = manager.IndexToNode(to_index)
        return uc * distance_matrix[u][v]

    transit_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    # -------- capacity constraint --------
    def demand_callback(from_index):
        return demands[manager.IndexToNode(from_index)]

    demand_idx = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_idx,
        0,
        capacities,   # mỗi xe capacity riêng
        True,
        "Capacity"
    )

    # -------- profit via disjunction --------
    for i in range(1, n + 1):
        index = manager.NodeToIndex(i)
        penalty = up * demands[i]   # mất revenue nếu bỏ khách
        routing.AddDisjunction([index], penalty)

    # -------- search --------
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.seconds = 3

    solution = routing.SolveWithParameters(params)

    if not solution:
        print(m)
        for _ in range(m):
            print(0)
        return

    # -------- output --------
    print(m)
    for v in range(m):
        idx = routing.Start(v)
        route = []
        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            if node != 0:
                route.append(node)
            idx = solution.Value(routing.NextVar(idx))

        print(len(route), *route)


if __name__ == "__main__":
    solve()