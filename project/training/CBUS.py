"""
Problem: CBUS (Passenger Bus Routing with Capacity)

Description:
- There are n passengers labeled 1...n.
- Each passenger i wants to travel from point i to point i+n.
- A bus starts at point 0 and must serve all passengers, finally returning to point 0.
- The bus has capacity k, meaning at most k passengers can be on the bus simultaneously.
- Distance matrix c is given, where c[i][j] is the travel distance from point i to j (0 <= i,j <= 2n).

Goal:
- Find the shortest possible route for the bus that:
  * Starts and ends at 0.
  * Picks up each passenger at point i and drops them at point i+n.
  * Never exceeds bus capacity at any point.

Input:
- Line 1: n, k (1 <= n <= 11, 1 <= k <= 10).
- Next (2n+1) lines: distance matrix c of size (2n+1) x (2n+1).

Output:
- A single line containing the length of the shortest route.

Example:
Input:
3 2
0 8 5 1 10 5 9
9 0 5 6 6 2 8
2 2 0 3 8 7 2
5 3 4 0 3 2 7
9 6 8 7 0 9 10
3 8 10 6 5 0 2
3 4 4 5 2 2 0

Output:
25
"""
from math import remainder


def solve(n, k, c, cmin):
    route = [-1] * (2*n + 1); route[0] = 0
    visited = [False] * (2*n + 1); visited[0] = True
    best = float('inf')
    curr_load, curr_cost = 0, 0

    def backtrack(node_idx):
        nonlocal route, visited, best, curr_load, curr_cost
        prev = route[node_idx - 1]

        if node_idx == (2*n + 1):
            total_cost = curr_cost + c[prev][0]
            if total_cost < best:
                best = total_cost
            return

        remaining = 2*n - node_idx + 1
        if curr_cost + remaining*cmin >= best:
            return

        for pos_idx in range(1, 2*n + 1):
            if not visited[pos_idx]:
                if pos_idx <= n: # pickup point
                    if curr_load < k:
                        route[node_idx] = pos_idx
                        visited[pos_idx] = True
                        curr_cost += c[prev][pos_idx]
                        curr_load += 1

                        backtrack(node_idx + 1)

                        curr_load -= 1
                        curr_cost -= c[prev][pos_idx]
                        visited[pos_idx] = False
                        route[node_idx] = -1
                else: # dropoff point
                    pickup = pos_idx - n
                    if visited[pickup]:
                        route[node_idx] = pos_idx
                        visited[pos_idx] = True
                        curr_cost += c[prev][pos_idx]
                        curr_load -= 1

                        backtrack(node_idx + 1)

                        curr_load += 1
                        curr_cost -= c[prev][pos_idx]
                        visited[pos_idx] = False
                        route[node_idx] = -1

    backtrack(1)
    return best

def main():
    import sys
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])

    size = 2*n + 1
    c = [[0]*size for _ in range(size)]
    cmin = float('inf')

    idx = 2
    for i in range(size):
        for j in range(size):
            val = int(data[idx]); idx += 1
            c[i][j] = val
            if i != j and val <= cmin:
                cmin = val

    result = solve(n, k, c, cmin)
    print(result)

if __name__ == '__main__':
    main()