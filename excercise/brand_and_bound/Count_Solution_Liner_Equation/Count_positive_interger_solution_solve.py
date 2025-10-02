"""
Problem: Count Positive Integer Solutions

Description:
Given a positive integer n and n positive integers a1, a2, ..., an,
compute the number of positive integer solutions (X1, X2, ..., Xn)
to the linear Diophantine equation:

    a1*X1 + a2*X2 + ... + an*Xn = M

Input:
- Line 1: Two integers n and M
- Line 2: n integers a1, a2, ..., an

Output:
- The number of positive integer solutions to the equation

Example:
Input:
3 5
1 1 1

Output:
6
"""
def count_positive_interger_solutions(n, M, a):
    """Đếm số nghiệm nguyên dương (X1..Xn) cho a1*X1 + ... + an*Xn = M"""
    def backtrack(k, curr_sum):
        if k == n:
            return 1 if curr_sum == M else 0

        total = 0
        max_val = (M - curr_sum) // a[k] # Xi >= 1 → thử từ 1 đến giới hạn
        for val in range(1, max_val + 1):
            total += backtrack(k + 1, curr_sum + a[k] * val)
        return total

    return backtrack(0, 0)

def main():
    import sys
    data = sys.stdin.read().strip().split()
    n, M = int(data[0]), int(data[1])
    a = list(map(int, data[2:]))

    result = count_positive_interger_solutions(n, M, a)
    print(result)

if __name__ == "__main__":
    main()