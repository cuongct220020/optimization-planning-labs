import sys
import os

from typing import Tuple



def is_valid():
    # passenger i: pickup = i, drop = i+N+M
    # parcel j: pickup = j+N, drop = j+2N+M
    # constraint 1: de tra hang thi can don hang
    # constraint 2: them hang khong vuot qua curr_load
    # constraint 3: neu don khach thi can tra khach luon
    pass

def bnb_share_a_ride_solve(N, M, K, q, Q, dist):
    size = 2*N + 2*M + 1
    routes = [[-1]*size for _ in range(K)]
    best_routes = [[-1] for _ in range(K)]
    curr_load = [0]*K
    curr_cost = [0]*K
    best_cost = [float('inf')]*K

    used_passengers = [False]*K
    used_parcels = [False]*K

    # requests = []
    # # Them vao hanh dong (don khach + tra khach)
    # for i in range(1, N):
    #     requests.append(Tuple(i, i + N + M))
    #
    #
    # # Them vao hanh don hang
    # for j in range(1, M):
    #     requests.append(j + N)
    #     requests.append(j + 2*N + M)


    # For each taxi
    for k in range (0, K):
        for v in range(0, size):
            def TRY(k, req):
                # For each passenger
                for i in range (1, N):
                    if is_valid():
                        last = routes[k][-1]
                        curr_cost[k] += dist[last][i]
                        used_passengers[k] = True

                        TRY(k, req + 1)

                        used_passengers[k] = False
                        curr_cost[k] -= dist[last][i]

                # For each parcels
                for j in range (1, M):
                    if is_valid():
                        last = routes[k][-1]
                        curr_cost[k] += dist[last][j]
                        curr_load[k] += q[j]
                        used_parcels[j] = True

                        TRY(k, req + 1)


                        used_parcels[j] = False
                        curr_load[k] -= q[j]
                        curr_cost[k] -= dist[last][j]




                if curr_cost[k] > best_cost:
                    best_cost = curr_cost[k]
                    # Gán route tốt nhất hiện tại
                    # best_routes[k] =



            TRY(0, 0)




if __name__ == '__main__':
    filename = "share_a_ride_solve.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()
    it = iter(data)

    N = int(next(it))       # N passenger requests
    M = int(next(it))       # M parcel requests
    K = int(next(it))       # K taxis

    q = []
    for _ in range(M):
        q.append(int(next(it)))

    Q = []
    for _ in range(K):
        Q.append(int(next(it)))

    dist = []
    size = 2*N + 2*M + 1
    for i in range(0, size):
        row = []
        for j in range(0, size):
            row.append(int(next(it)))
        dist.append(row)

    bnb_share_a_ride_solve(N, M, K, q, Q, dist)