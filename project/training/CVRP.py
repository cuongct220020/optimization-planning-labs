"""
Problem: Capacitated Vehicle Routing (CVRP)

Description:
- There are n clients labeled 1..n, each client i requests d[i] packages.
- A fleet of K identical trucks (capacity Q each) must deliver packages.
- All trucks start from the central depot (node 0), serve some clients, and return to the depot.
- Each client must be visited by exactly one truck.
- The demand served by a truck cannot exceed its capacity Q.
- A truck may have an empty route (visit no clients).
- Order of visiting clients matters (different permutations yield different distances).
- Distance matrix c[i][j] is given for 0 <= i,j <= n.

Goal:
- Find a set of routes (one per truck) that minimizes the total travel distance.

Input:
- Line 1: n, K, Q (2 <= n <= 12, 1 <= K <= 5, 1 <= Q <= 50).
- Line 2: d[1] .. d[n], the demand of each client (1 <= d[i] <= 10).
- Next (n+1) lines: the (n+1) x (n+1) distance matrix (1 <= c[i][j] <= 30).

Output:
- Minimal total travel distance.

Example:
Input:
4 2 15
7 7 11 2
0 12 12 11 14
14 0 11 14 14
14 10 0 11 12
10 14 12 0 13
10 13 14 11 0

Output:
70
"""
