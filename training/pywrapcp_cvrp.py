import sys
import os

from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve():
    filename = "cvrp_input.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))
    K = int(next(it))
    Q = int(next(it))

    demands = [0] * (n + 1)
    for i in range(1, n + 1):
        demands[i] = int(next(it))

    distance_matrix = []
    for _ in range(n + 1):
        row = []
        for _ in range(n + 1):
            row.append(int(next(it)))
        distance_matrix.append(row)

    manager = pywrapcp.RoutingIndexManager(n + 1, K, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return demands[manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, [Q] * K, True, "Capacity"
    )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )
    search_parameters.time_limit.seconds = 1

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print(int(solution.ObjectiveValue()))


if __name__ == "__main__":
    solve()