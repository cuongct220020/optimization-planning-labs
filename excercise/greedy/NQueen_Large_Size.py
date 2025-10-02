def solve_n_queens(n):
    if n == 2 or n == 3:
        return []  # không có nghiệm

    solution = []

    if n % 6 != 2 and n % 6 != 3:
        # Dãy: 2,4,6,...,n, 1,3,5,...,n
        solution = list(range(2, n+1, 2)) + list(range(1, n+1, 2))
    elif n % 6 == 2:
        # Hoán vị đặc biệt
        solution = list(range(2, n+1, 2)) + [3, 1] + list(range(7, n+1, 2)) + [5]
    elif n % 6 == 3:
        # Hoán vị đặc biệt
        solution = [2, 4, 6] + list(range(8, n+1, 2)) + [1, 3] + list(range(7, n+1, 2)) + [5]

    return solution


def main():
    n = int(input().strip())
    solution = solve_n_queens(n)
    print(n)
    print(" ".join(map(str, solution)))


if __name__ == "__main__":
    main()