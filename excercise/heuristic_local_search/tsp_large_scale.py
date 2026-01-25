import sys
import os
import math
import random
import time


def solve():
    filename = "tsp_input.txt"

    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()
    it = iter(data)

    n = int(next(it))
    dist = [[float(next(it)) for _ in range(n)] for __ in range(n)]

    # 1. NEAREST NEIGHBOR INITIAL SOLUTION
    visited = [False] * n
    path = [0]
    visited[0] = True

    for _ in range(n - 1):
        last = path[-1]
        best = -1
        best_d = float('inf')

        for j in range(n):
            if not visited[j] and dist[last][j] < best_d:
                best_d = dist[last][j]
                best = j

        path.append(best)
        visited[best] = True

    def tour_cost(p):
        s = 0.0
        for i in range(n):
            s += dist[p[i]][p[(i + 1) % n]]
        return s

    cur_cost = tour_cost(path)
    best_path = path[:]
    best_cost = cur_cost

    # 2. SIMULATED ANNEALING + 2-OPT
    T = 800.0
    cooling = 0.9993
    Tmin = 1e-6

    start = time.time()
    TIME_LIMIT = 1.9

    while time.time() - start < TIME_LIMIT and T > Tmin:
        i = random.randint(0, n - 3)
        j = random.randint(i + 2, n - 1)

        # tránh đảo toàn bộ vòng
        if i == 0 and j == n - 1:
            continue

        a = path[i]
        b = path[i + 1]
        c = path[j]
        d = path[(j + 1) % n]

        delta = dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]

        if delta < 0 or random.random() < math.exp(-delta / T):
            path[i + 1: j + 1] = reversed(path[i + 1: j + 1])
            cur_cost += delta

            if cur_cost < best_cost:
                best_cost = cur_cost
                best_path = path[:]

        T *= cooling

    print(n)
    print(*[x + 1 for x in best_path])


if __name__ == "__main__":
    solve()
