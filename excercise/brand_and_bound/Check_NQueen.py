def check_board(N, board):
    rows = set()
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    queens = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                # kiểm tra ngay khi thêm quân hậu
                if i in rows or j in cols or (i - j) in diag1 or (i + j) in diag2:
                    return 0
                rows.add(i)
                cols.add(j)
                diag1.add(i - j)
                diag2.add(i + j)
                queens.append((i, j))

    # Nếu có đúng N quân hậu và không tấn công nhau
    return 1 if len(queens) == N else 0


def main():
    T = int(input().strip())
    for _ in range(T):
        N = int(input().strip())
        board = []
        for _ in range(N):
            row = list(map(int, input().split()))
            board.append(row)
        print(check_board(N, board))


if __name__ == "__main__":
    main()
