import sys
import os

V = -1
E = -1
M = -1
adj = []

x = []
colored = []


def is_safe(v, c):
    for u in adj[v]:
        if x[u] == c:
            return False
    return True


def solve(v):
    if v == V:
        return True

    for c in range(1, M + 1):
        if is_safe(v, c):
            x[v] = c
            if solve(v + 1):
                return True
            x[v] = -1

    return False



if __name__ == '__main__':
    filename = "graph_coloring_input.txt"
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)

    V = int(next(it))
    E = int(next(it))
    M = int(next(it))

    adj = [[] for _ in range(V)]
    x = [-1] * V
    colored = [-1] * V

    for _ in range(E):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    if solve(0):
        print("YES")
    else:
        print("NO")