"""
Problem: N-Queens Validation

Description:
Given a chessboard of size N x N with exactly N queens placed in N different cells,
the task is to check if the placement is valid — i.e., no two queens can attack each other.

Rules of attack:
- Two queens attack each other if they share the same row, the same column,
  or lie on the same diagonal (both main and anti-diagonal).

Input:
- The first line contains a positive integer T (1 <= T <= 100), the number of test cases.
- Each test case has the following format:
  - The first line contains a positive integer N (1 <= N <= 100).
  - The next N lines each contain N integers (0 or 1), representing the board:
    * A[i][j] = 1 if there is a queen at cell (i, j).
    * A[i][j] = 0 otherwise.

Output:
- For each test case, print 1 if the placement is valid (no queens attack each other).
- Print 0 otherwise.

Example:
Input:
2
4
0 1 0 0
0 0 0 1
1 0 0 0
0 0 1 0
4
0 1 0 0
0 0 0 0
1 0 0 1
0 0 1 0

Output:
1
0
"""
def check(board):
    n = len(board)
    rows = set()
    cols = set()
    diag1 = set() # r - c
    diag2 = set() # r + c

    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:
                if r in rows or c in cols or (r-c) in diag1 or (r+c) in diag2:
                    return 0
                rows.add(r)
                cols.add(c)
                diag1.add(r-c)
                diag2.add(r+c)

    return 1

def solve():
    import sys
    data = sys.stdin.read().strip().split()

    it = iter(data)
    T = int(next(it))
    for _ in range(T):
        n = int(next(it))
        board = [[int(next(it)) for _ in range(n)] for _ in range(n)]
        print(check(board))

if __name__ == "__main__":
    solve()
