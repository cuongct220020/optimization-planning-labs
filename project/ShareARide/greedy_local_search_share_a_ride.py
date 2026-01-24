import sys
import os
import copy


def calculate_route_distance(route, dist):
    """Tính tổng khoảng cách của một route"""
    total = 0
    for i in range(len(route) - 1):
        total += dist[route[i]][route[i + 1]]
    return total


def greedy_construct(N, M, K, q, Q, dist):
    """Xây dựng solution ban đầu bằng greedy min-max"""
    passengers_served = [False] * (N + 1)
    parcels_picked = [False] * (M + 1)
    parcels_delivered = [False] * (M + 1)

    taxi_routes = [[0] for _ in range(K + 1)]
    taxi_load = [0] * (K + 1)
    taxi_dist = [0] * (K + 1)
    taxi_parcels = [set() for _ in range(K + 1)]
    taxi_pos = [0] * (K + 1)

    finished_request = 0
    total_requests = N + M

    while finished_request < total_requests:
        best_taxi = -1
        best_req_idx = -1
        best_action = ""
        best_points = []
        best_increase = 0
        min_max_dist = float('inf')

        for k in range(1, K + 1):
            for i in range(1, N + 1):
                if not passengers_served[i]:
                    pickup = i
                    dropoff = i + N + M
                    increase = dist[taxi_pos[k]][pickup] + dist[pickup][dropoff]
                    new_dist = taxi_dist[k] + increase
                    max_dist = max(new_dist, max(taxi_dist[1:K + 1]))

                    if max_dist < min_max_dist:
                        min_max_dist = max_dist
                        best_taxi = k
                        best_req_idx = i
                        best_action = "passenger"
                        best_points = [pickup, dropoff]
                        best_increase = increase

            for j in range(1, M + 1):
                if not parcels_picked[j] and taxi_load[k] + q[j] <= Q[k]:
                    pickup = j + N
                    increase = dist[taxi_pos[k]][pickup]
                    new_dist = taxi_dist[k] + increase
                    max_dist = max(new_dist, max(taxi_dist[1:K + 1]))

                    if max_dist < min_max_dist:
                        min_max_dist = max_dist
                        best_taxi = k
                        best_req_idx = j
                        best_action = "parcel_pickup"
                        best_points = [pickup]
                        best_increase = increase

            for j in taxi_parcels[k]:
                dropoff = j + 2 * N + M
                increase = dist[taxi_pos[k]][dropoff]
                new_dist = taxi_dist[k] + increase
                max_dist = max(new_dist, max(taxi_dist[1:K + 1]))

                if max_dist < min_max_dist:
                    min_max_dist = max_dist
                    best_taxi = k
                    best_req_idx = j
                    best_action = "parcel_drop"
                    best_points = [dropoff]
                    best_increase = increase

        if best_taxi != -1:
            if best_action == "passenger":
                taxi_routes[best_taxi].extend(best_points)
                taxi_dist[best_taxi] += best_increase
                taxi_pos[best_taxi] = best_points[-1]
                passengers_served[best_req_idx] = True
                finished_request += 1
            elif best_action == "parcel_pickup":
                taxi_routes[best_taxi].extend(best_points)
                taxi_dist[best_taxi] += best_increase
                taxi_pos[best_taxi] = best_points[-1]
                taxi_load[best_taxi] += q[best_req_idx]
                taxi_parcels[best_taxi].add(best_req_idx)
                parcels_picked[best_req_idx] = True
            elif best_action == "parcel_drop":
                taxi_routes[best_taxi].extend(best_points)
                taxi_dist[best_taxi] += best_increase
                taxi_pos[best_taxi] = best_points[-1]
                taxi_load[best_taxi] -= q[best_req_idx]
                taxi_parcels[best_taxi].remove(best_req_idx)
                parcels_delivered[best_req_idx] = True
                finished_request += 1
        else:
            break

    return taxi_routes


def swap_requests_between_taxis(routes, dist, N, M, K):
    """
    Thử hoán đổi requests giữa các taxi để cải thiện max distance
    """
    improved = True
    iterations = 0
    max_iterations = 100

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1

        # Tính khoảng cách hiện tại
        current_dists = [0] * (K + 1)
        for k in range(1, K + 1):
            current_dists[k] = calculate_route_distance(routes[k], dist)
        current_max = max(current_dists[1:K + 1])

        # Thử swap giữa từng cặp taxi
        for k1 in range(1, K + 1):
            for k2 in range(k1 + 1, K + 1):
                # Thử swap từng passenger
                for i in range(1, N + 1):
                    pickup = i
                    dropoff = i + N + M

                    # Kiểm tra nếu passenger i thuộc taxi k1
                    if pickup in routes[k1] and dropoff in routes[k1]:
                        # Thử chuyển sang taxi k2
                        new_routes = copy.deepcopy(routes)
                        new_routes[k1].remove(pickup)
                        new_routes[k1].remove(dropoff)

                        # Chèn vào vị trí tốt nhất trong route k2
                        best_pos = 1
                        best_dist = float('inf')
                        for pos in range(1, len(new_routes[k2])):
                            test_route = new_routes[k2][:pos] + [pickup, dropoff] + new_routes[k2][pos:]
                            d = calculate_route_distance(test_route, dist)
                            if d < best_dist:
                                best_dist = d
                                best_pos = pos

                        new_routes[k2] = new_routes[k2][:best_pos] + [pickup, dropoff] + new_routes[k2][best_pos:]

                        # Tính max distance mới
                        new_dists = [0] * (K + 1)
                        for k in range(1, K + 1):
                            new_dists[k] = calculate_route_distance(new_routes[k], dist)
                        new_max = max(new_dists[1:K + 1])

                        # Chấp nhận nếu cải thiện
                        if new_max < current_max:
                            routes = new_routes
                            current_max = new_max
                            improved = True

    return routes


def local_search_solve(N, M, K, q, Q, dist):
    """Greedy + Local Search"""
    # Bước 1: Xây dựng solution ban đầu
    routes = greedy_construct(N, M, K, q, Q, dist)

    # Bước 2: Cải thiện bằng local search
    routes = swap_requests_between_taxis(routes, dist, N, M, K)

    # In kết quả
    print(K)
    for k in range(1, K + 1):
        if routes[k][-1] != 0:
            routes[k].append(0)
        print(len(routes[k]))
        print(*routes[k])


if __name__ == '__main__':
    filename = "share_a_ride_solve.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()
    it = iter(data)

    N = int(next(it))
    M = int(next(it))
    K = int(next(it))

    q = [0] * (M + 1)
    for i in range(1, M + 1):
        q[i] = int(next(it))

    Q = [0] * (K + 1)
    for i in range(1, K + 1):
        Q[i] = int(next(it))

    size = 2 * N + 2 * M + 1
    dist = [[0] * size for _ in range(size)]
    for i in range(0, size):
        for j in range(0, size):
            dist[i][j] = int(next(it))

    local_search_solve(N, M, K, q, Q, dist)