import sys
import os
import random


def solve():
    filename = "nqueen_input.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()

    it = iter(data)
    n = int(next(it))

    queens = [-1] * n

    rows = [0] * n
    diag1 = [0] * (2 * n - 1)   # r - c + n - 1
    diag2 = [0] * (2 * n - 1)   # r + c

    def conflicts(r, c):
        return rows[r] + diag1[r - c + n - 1] + diag2[r + c]

    # Greedy init (sampling)
    sample_size = 40
    all_rows = list(range(n))

    for c in range(n):
        best = []
        min_c = 10**18

        if n <= sample_size:
            sample = all_rows
        else:
            sample = random.sample(all_rows, sample_size)

        for r in sample:
            v = conflicts(r, c)
            if v < min_c:
                min_c = v
                best = [r]
            elif v == min_c:
                best.append(r)

        r0 = random.choice(best)
        queens[c] = r0

        rows[r0] += 1
        diag1[r0 - c + n - 1] += 1
        diag2[r0 + c] += 1

    # Min-Conflicts Loop
    max_steps = 3 * n

    for _ in range(max_steps):
        conflicted = []

        for c in range(n):
            r = queens[c]
            sc = rows[r] + diag1[r - c + n - 1] + diag2[r + c] - 3
            if sc > 0:
                conflicted.append(c)

        if not conflicted:
            break

        c = random.choice(conflicted)
        old_r = queens[c]

        rows[old_r] -= 1
        diag1[old_r - c + n - 1] -= 1
        diag2[old_r + c] -= 1

        # random walk 3%
        if random.random() < 0.03:
            new_r = random.randint(0, n - 1)
        else:
            best = []
            min_c = 10**18

            # Optimization: ưu tiên hàng trống
            for r in range(n):
                v = rows[r] + diag1[r - c + n - 1] + diag2[r + c]
                if v < min_c:
                    min_c = v
                    best = [r]
                elif v == min_c:
                    best.append(r)

            new_r = random.choice(best)

        queens[c] = new_r
        rows[new_r] += 1
        diag1[new_r - c + n - 1] += 1
        diag2[new_r + c] += 1

    print(n)
    print(*[x + 1 for x in queens])


if __name__ == "__main__":
    solve()
