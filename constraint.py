import argparse, json, itertools

def solve(variables, domains, constraints):
    """Simple backtracking CSP solver"""
    assignment = {}
    def consistent(var, val):
        assignment[var] = val
        for (v1, op, v2) in constraints:
            if v1 in assignment and v2 in assignment:
                a, b = assignment[v1], assignment[v2]
                if op == "!=" and a == b: del assignment[var]; return False
                if op == "==" and a != b: del assignment[var]; return False
                if op == "<" and a >= b: del assignment[var]; return False
                if op == ">" and a <= b: del assignment[var]; return False
        del assignment[var]
        return True
    def backtrack(i):
        if i == len(variables): return dict(assignment)
        var = variables[i]
        for val in domains[var]:
            if consistent(var, val):
                assignment[var] = val
                result = backtrack(i + 1)
                if result: return result
                del assignment[var]
        return None
    return backtrack(0)

def main():
    p = argparse.ArgumentParser(description="CSP solver")
    p.add_argument("file", nargs="?", help="JSON CSP definition")
    p.add_argument("--nqueens", type=int, help="Solve N-Queens")
    args = p.parse_args()
    if args.nqueens:
        n = args.nqueens
        variables = [f"q{i}" for i in range(n)]
        domains = {v: list(range(n)) for v in variables}
        constraints = []
        for i in range(n):
            for j in range(i+1, n):
                constraints.append((f"q{i}", "!=", f"q{j}"))
        result = solve(variables, domains, constraints)
        # Post-check diagonals
        if result:
            for i in range(n):
                for j in range(i+1, n):
                    if abs(result[f"q{i}"] - result[f"q{j}"]) == j - i:
                        result = None; break
                if not result: break
        if result:
            for i in range(n):
                row = ["." if j != result[f"q{i}"] else "Q" for j in range(n)]
                print(" ".join(row))
        else:
            print("No solution found")
    elif args.file:
        csp = json.load(open(args.file))
        result = solve(csp["variables"], csp["domains"], [tuple(c) for c in csp["constraints"]])
        if result: print(json.dumps(result, indent=2))
        else: print("No solution")
    else: p.print_help()

if __name__ == "__main__":
    main()
