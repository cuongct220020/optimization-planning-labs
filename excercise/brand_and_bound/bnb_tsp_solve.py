"""
Problem: Traveling Salesman Problem (TSP) - Branch and Bound

Description:
- There are n cities numbered from 1 to n.
- The travel distance between city i and city j is given by the matrix c(i,j).
- A salesman starts from city 1, visits each city 2..n exactly once,
  and then returns to city 1.
- The goal is to find the itinerary (tour) with the minimal total travel distance.

Input:
- Line 1: a positive integer n (1 <= n <= 20)
- Next n lines: the distance matrix of size n x n,
  where the element at row i and column j is c(i,j).

Output:
- Print a single integer: the total minimal travel distance of the optimal tour.

Example:
Input
4
0 1 1 9
1 0 9 3
1 9 0 2
9 3 2 0

Output
7

Explanation:
- The optimal tour is 1 -> 2 -> 4 -> 3 -> 1
- Total distance = c(1,2) + c(2,4) + c(4,3) + c(3,1)
                 = 1 + 3 + 2 + 1 = 7
"""

def tsp_bnb_solve(n, c, cmin):
    visited = [False] * (n + 1)
    route = [-1] * (n + 1); route[1] = 1
    best_cost = float('inf')
    curr_cost = 0

    def back_tracking(node):
        nonlocal route, visited, best_cost, curr_cost
        prev = route[node - 1]

        if node == (n + 1):
            total_cost = curr_cost + c[prev][1]
            if total_cost < best_cost:
                best_cost = total_cost
            return

        remaining = n - node + 1
        if curr_cost + remaining*cmin >= best_cost:
            return

        for pos in range(2, n + 1):
            if visited[pos]:
                continue

            route[node] = pos
            visited[pos] = True
            curr_cost += c[prev][pos]

            back_tracking(node + 1)

            curr_cost -= c[prev][pos]
            visited[pos] = False
            route[node] = -1

    back_tracking(2)
    return best_cost

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])

    size = n + 1
    c = [[0] * size for _ in range(size)]
    cmin = float('inf')

    idx = 1
    for i in range(1, size):
        for j in range(1, size):
            val = int(data[idx]); idx += 1
            c[i][j] = val
            if i != j and  cmin > val:
                cmin = val

    result = tsp_bnb_solve(n, c, cmin)
    print(result)

if __name__ == "__main__":
    main()