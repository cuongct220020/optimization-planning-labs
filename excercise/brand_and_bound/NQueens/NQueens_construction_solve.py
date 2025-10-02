"""
Problem: N-Queens Construction (Large N)

Description:
Find a solution to place n queens on an n x n chess board such that no two queens attack each other.
- Each queen must be placed in a unique row and a unique column.
- No two queens can share the same diagonal.

Representation:
A solution is represented as a sequence of integers:
    x[1], x[2], ..., x[n]
where x[i] is the row index of the queen placed in column i (1 <= i <= n).

Input:
- Line 1: contains a positive integer n (10 <= n <= 10000).

Output:
- Line 1: print n
- Line 2: print the sequence x[1], x[2], ..., x[n], separated by spaces.

Constraints:
- The size n is large, so the algorithm must be efficient (O(n) or O(n log n)).
- Direct backtracking or naive DFS will not work for n up to 10000.

Example:
Input:
10

Output:
9 2 4 1 7 10 6 3 5 8
"""

def check(r, x, c_idx):
    for i in range(c_idx):
        if x[i] == r or abs(x[i] - r) == abs(i - c_idx):
            return False
    return True

def backtrack(n, x, c_idx):
    if c_idx == n:
        print(" ".join(str(v+1) for v in x))  # xuất nghiệm
        exit(0)
    for r in range(n):
        if check(r, x, c_idx):
            x[c_idx] = r
            backtrack(n, x, c_idx + 1)
            x[c_idx] = 0

def main():
    import sys
    n = int(sys.stdin.readline())
    x = [0] * n
    backtrack(n, x, 0)

if __name__ == '__main__':
    main()
