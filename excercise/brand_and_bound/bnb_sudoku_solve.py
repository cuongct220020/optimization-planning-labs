"""
Problem: Count Sudoku Solutions

Description:
Given a partially filled 9x9 Sudoku grid, compute the total number of valid
solutions by filling in the empty cells (denoted by 0). A valid Sudoku solution
must satisfy the following rules:
- Each row must contain distinct numbers from 1 to 9.
- Each column must contain distinct numbers from 1 to 9.
- Each 3x3 sub-grid must contain distinct numbers from 1 to 9.

Input:
- 9 lines, each containing 9 integers (values between 0 and 9).
- A value of 0 indicates an empty cell.

Output:
- An integer representing the number of valid Sudoku solutions for the given grid.

Example:
Input:
0 0 3 4 0 0 0 8 9
0 0 6 7 8 9 0 2 3
0 8 0 0 2 3 4 5 6
0 0 4 0 6 5 0 9 7
0 6 0 0 9 0 0 1 4
0 0 7 2 0 4 3 6 5
0 3 0 6 0 2 0 7 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0

Output:
64
"""
def count_sudoku_solutions(grid):
    """Count the number of valid Sudoku solutions using backtracking."""
    count_solutions = 0

    def check_grid(row, col, val):
        """Check if placing val at (row, col) is valid."""
        # Check column
        for i in range(9):
            if grid[i][col] == val:
                return False
        # Check row
        for j in range(9):
            if grid[row][j] == val:
                return False
        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == val:
                    return False
        return True

    def back_tracking(i, j):
        nonlocal count_solutions

        if i == 9:  # finished all rows -> found a solution
            count_solutions += 1
            return

        # Next cell
        next_i, next_j = (i, j + 1) if j < 8 else (i + 1, 0)

        if grid[i][j] != 0:
            back_tracking(next_i, next_j)
        else:
            for val in range(1, 10):
                if check_grid(i, j, val):
                    grid[i][j] = val
                    back_tracking(next_i, next_j)
                    grid[i][j] = 0  # backtrack

    # Start from top-left corner
    back_tracking(0, 0)
    return count_solutions


def main():
    import sys
    grid = [list(map(int, sys.stdin.readline().split())) for _ in range(9)]
    result = count_sudoku_solutions(grid)
    print(result)


if __name__ == '__main__':
    main()