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

def CBUS_solve(n, max_load, cost, c_min):
    visited = [False] * (2*n + 1)
    best_cost = float("inf")
    curr_cost, curr_load = 0, 0

    def back_tracking(curr_pos, served_count):
        nonlocal visited, best_cost, curr_cost, curr_load

        # Nếu đã thăm hết các điểm (2n khách), quay về 0
        if served_count == 2*n:
            total_cost = curr_cost + cost[curr_pos][0]
            best_cost = min(best_cost, total_cost)
            return

        # pruning
        if curr_cost + (2*n - served_count + 1) * c_min >= best_cost:
            return

        for nxt in range(1, 2*n + 1):
            if not visited[nxt]:
                if nxt <= n:  # pick-up point
                    if curr_load < max_load:
                        visited[nxt] = True
                        curr_cost += cost[curr_pos][nxt]
                        curr_load += 1

                        back_tracking(nxt, served_count + 1)

                        curr_load -= 1
                        curr_cost -= cost[curr_pos][nxt]
                        visited[nxt] = False

                else:  # drop-off point
                    if visited[nxt - n]:  # chỉ được trả nếu đã đón
                        visited[nxt] = True
                        curr_cost += cost[curr_pos][nxt]
                        curr_load -= 1

                        back_tracking(nxt, served_count + 1)

                        curr_load += 1
                        curr_cost -= cost[curr_pos][nxt]
                        visited[nxt] = False

    back_tracking(0, 0)
    return best_cost

def main():
    import sys
    data = sys.stdin.read().split()

    n, k = int(data[0]), int (data[1])
    size = 2*n + 1
    cost = [[0] * size for _ in range(size)]
    c_min = float('inf')

    idx = 2
    for i in range(size):
        for j in range(size):
            val = int(data[idx]); idx += 1
            cost[i][j] = val
            if i != j and val < c_min:
                c_min = val

    result = CBUS_solve(n, k, cost, c_min)
    print(result)

if __name__ == '__main__':
    main()