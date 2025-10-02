"""
Problem: CBUS (Passenger Bus Routing with Capacity)

Description:
- There are n passengers labeled 1..n.
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