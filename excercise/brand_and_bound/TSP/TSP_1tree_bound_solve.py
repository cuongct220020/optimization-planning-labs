# Branch-and-Bound TSP with 1-tree lower bound (uses undirected weights w[i][j]=min(c[i][j],c[j][i]))

from math import inf

def tsp_bnb_1tree(n, c):
    # 1-based indexing: c is (n+1)x(n+1)
    # Build undirected weights (conservative for asymmetric graphs)
    w = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                w[i][j] = 0
            else:
                w[i][j] = min(c[i][j], c[j][i])

    visited = [False] * (n + 1)
    visited[1] = True
    route = [-1] * (n + 1)
    route[1] = 1
    best = [inf]
    curr_cost = 0

    # MST cost on nodes_excl_root: list of node ids (using undirected weights w)
    def mst_cost(nodes_excl_root):
        m = len(nodes_excl_root)
        if m == 0:
            return 0.0
        in_mst = [False] * m
        key = [inf] * m
        key[0] = 0.0
        total = 0.0
        for _ in range(m):
            u_idx = -1
            minkey = inf
            for i in range(m):
                if not in_mst[i] and key[i] < minkey:
                    minkey = key[i];
                    u_idx = i
            if u_idx == -1:
                return inf
            in_mst[u_idx] = True
            total += key[u_idx]
            u_node = nodes_excl_root[u_idx]
            for v_idx in range(m):
                if not in_mst[v_idx]:
                    v_node = nodes_excl_root[v_idx]
                    if w[u_node][v_node] < key[v_idx]:
                        key[v_idx] = w[u_node][v_node]
        return total

    # compute 1-tree lower bound for remaining nodes: S = {1} U Unvisited U {prev}
    def one_tree_lb(prev):
        # build set S
        S_set = {1, prev}
        for v in range(2, n + 1):
            if not visited[v]:
                S_set.add(v)
        # nodes_excl_root are S \ {1}
        nodes_excl_root = [v for v in S_set if v != 1]
        m = len(nodes_excl_root)
        if m == 0:
            return 0.0  # nothing remaining
        # MST on nodes_excl_root
        mst = mst_cost(nodes_excl_root)
        # two smallest edges from root 1 to nodes_excl_root (using w)
        mins = sorted((w[1][v] for v in nodes_excl_root))
        if len(mins) == 1:
            s1 = s2 = mins[0]
        else:
            s1, s2 = mins[0], mins[1]
        one_tree = mst + s1 + s2
        # convert cycle bound to path bound (path from prev -> ... -> 1)
        lb_path = one_tree - w[1][prev]
        # numerical rounding safety
        if lb_path < 0:
            lb_path = 0.0
        return lb_path

    # heuristic order of next nodes by increasing edge from prev
    def candidates_order(prev):
        cand = []
        for v in range(2, n + 1):
            if not visited[v]:
                cand.append((c[prev][v], v))
        cand.sort()
        return [v for _, v in cand]

    def backtrack(node, prev):
        nonlocal curr_cost
        # node is the position we're filling (2..n)
        if node == n + 1:
            total = curr_cost + c[prev][1]
            if total < best[0]:
                best[0] = total
            return

        # compute LB using 1-tree
        lb_remaining = one_tree_lb(prev)
        if curr_cost + lb_remaining >= best[0]:
            return

        for v in candidates_order(prev):
            route[node] = v
            visited[v] = True
            curr_cost += c[prev][v]

            backtrack(node + 1, v)

            curr_cost -= c[prev][v]
            visited[v] = False
            route[node] = -1

    backtrack(2, 1)
    return int(best[0]) if best[0] < inf else None

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])

    size = n + 1
    c = [[0] * size for _ in range(size)]
    cmin = float('inf')

    idx = 1
    for i in range(1, size):
        for j in range(1, size):
            val = int(data[idx]); idx += 1
            c[i][j] = val
            if i != j and  cmin > val:
                cmin = val

    result = tsp_bnb_1tree(n, c)
    print(result)

if __name__ == "__main__":
    main()