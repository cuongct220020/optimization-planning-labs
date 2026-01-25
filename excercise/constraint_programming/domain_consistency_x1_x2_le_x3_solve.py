import sys
import os


if __name__ == '__main__':
    filename = "domain_consistency_input.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = f.read().splitlines()
    else:
        data = sys.stdin.read().splitlines()

    domains = []
    for line in data:
        if line.strip():
            d = sorted([int(x) for x in line.split()])
            domains.append(d)

    d1, d2, d3 = domains
    min_d1, max_d1 = min(d1), max(d1)
    min_d2, max_d2 = min(d2), max(d2)
    min_d3, max_d3 = min(d3), max(d3)

    new_d1, new_d2, new_d3 = [], [], []

    # Lọc value của d1
    for v in d1:
        if v + min_d2 <= max_d3:
            new_d1.append(v)

    # Lọc value của d2
    for v in d2:
        if min_d1 + v <= max_d3:
            new_d2.append(v)

    # Lọc value của d3
    for v in d3:
        if min_d1 + min_d2 <= v:
            new_d3.append(v)


    print(" ".join(map(str, new_d1)))
    print(" ".join(map(str, new_d2)))
    print(" ".join(map(str, new_d3)))