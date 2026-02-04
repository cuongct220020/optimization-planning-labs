"""
Problem: Min-Max Vehicle Routing Problem (Min_Max_VRP)

Description:
- There are N locations labeled 1..N that need parcel collection.
- K postmen (vehicles) start from the post office (location 0).
- The distance between any two points i and j (0 <= i,j <= N) is given by the matrix d.
- Each postman must be assigned a route starting from 0, visiting some subset of locations in some order,
  and then returning to 0.
- The objective is to minimize the maximum route length among all K postmen
  (i.e., balance the workload so that the longest route is as short as possible).

Representation of a solution:
- A solution consists of K routes, one for each postman.
- Each route k is represented by a sequence of integers:
    x[1], x[2], ..., x[lk]
  where:
    * x[1] = 0 (the starting depot),
    * x[2]..x[lk] are the collection points visited by this postman.

Input:
- Line 1: N, K (1 <= N <= 1000, 1 <= K <= 100).
- Next (N+1) lines: the distance matrix d of size (N+1) x (N+1).

Output:
- Line 1: the integer K.
- For each postman k = 1..K:
    Line 2*k: the integer lk (length of the route).
    Line 2*k+1: the sequence of integers x[1]..x[lk], separated by spaces.

Goal:
- Minimize the length of the longest route among all K postmen.

Example:
Input:
6 2
0 9 9 9 7 2 9
9 0 3 0 2 8 1
9 3 0 3 4 7 4
9 0 3 0 2 8 1
7 2 4 2 0 6 2
2 8 7 8 6 0 8
9 1 4 1 2 8 0

Output:
2
3
0 5 2
5
0 4 1 3 6
"""