"""
Exhaustive enumeration of all meta-rules for n=2.

For n=2: |X|=2, |F|=4, so a meta-rule phi: F x X -> F
is a function from 8 inputs to 4 outputs = 4^8 = 65536 possible meta-rules.

We classify each by the structure of the resulting dynamical system:
- Number of fixed points
- Number and lengths of cycles
- Maximum transient length
- Function diversity (how many distinct f appear in orbits)

Goal: find which meta-rules produce the most "creative" dynamics.
"""

import itertools
import json
import os
from collections import Counter
from dds import (
    Func, State, enumerate_functions, analyze_system, step,
)
from visualize import orbit_complexity_measures


def enumerate_all_meta_rules(n: int):
    """Yield all possible meta-rules phi: F x X -> F for given n.

    Each meta-rule is represented as a tuple of |F|*|X| function indices.
    """
    funcs = enumerate_functions(n)
    num_inputs = len(funcs) * n  # |F| * |X|
    num_outputs = len(funcs)     # |F|

    # Each meta-rule is a tuple of num_inputs values, each in range(num_outputs)
    for combo in itertools.product(range(num_outputs), repeat=num_inputs):
        yield combo


def meta_rule_from_tuple(combo: tuple, funcs: list[Func], n: int):
    """Convert a tuple representation to a callable meta-rule."""
    # Build a lookup: (f_index, x) -> func_index
    lookup = {}
    idx = 0
    for fi, f in enumerate(funcs):
        for x in range(n):
            lookup[(f.table, x)] = funcs[combo[idx]]
            idx += 1

    def phi(f: Func, x: int) -> Func:
        return lookup[(f.table, x)]
    return phi


def classify_meta_rule(combo: tuple, funcs: list[Func], n: int) -> dict:
    """Classify a single meta-rule by its dynamical properties."""
    phi = meta_rule_from_tuple(combo, funcs, n)

    total_states = len(funcs) * n
    # Compute the functional graph
    graph = {}
    for f in funcs:
        for x in range(n):
            s = State(f, x)
            s_next = step(s, phi)
            graph[(f.table, x)] = (s_next.f.table, s_next.x)

    # Find cycles by following each node
    visited = {}
    cycles = []
    fixed_points = 0
    max_transient = 0
    total_distinct_f = set()

    for f in funcs:
        for x in range(n):
            start = (f.table, x)
            if start in visited:
                continue

            path = []
            path_set = {}
            node = start
            while node not in visited and node not in path_set:
                path_set[node] = len(path)
                path.append(node)
                node = graph[node]

            if node in path_set:
                cycle_start = path_set[node]
                cycle_len = len(path) - cycle_start
                transient = cycle_start
                cycle_nodes = path[cycle_start:]

                if cycle_len == 1:
                    fixed_points += 1
                else:
                    cycles.append(cycle_len)

                max_transient = max(max_transient, transient)

                for n_ in path:
                    visited[n_] = True
                    total_distinct_f.add(n_[0])
            else:
                # Reached already-visited node
                for n_ in path:
                    visited[n_] = True
                    total_distinct_f.add(n_[0])

    # Unique cycle lengths (sorted)
    cycle_lengths = sorted(set(cycles)) if cycles else []

    return {
        "combo": combo,
        "fixed_points": fixed_points,
        "num_cycles": len(set(cycles)),
        "cycle_lengths": cycle_lengths,
        "max_cycle": max(cycles) if cycles else (1 if fixed_points > 0 else 0),
        "max_transient": max_transient,
        "distinct_functions": len(total_distinct_f),
        "total_states": total_states,
    }


def run_exhaustive_n2():
    """Enumerate all 65536 meta-rules for n=2 and classify them."""
    n = 2
    funcs = enumerate_functions(n)
    print(f"Enumerating all meta-rules for n={n}")
    print(f"|F| = {len(funcs)}, |X| = {n}")
    print(f"|F x X| = {len(funcs) * n} (input space of phi)")
    print(f"Total meta-rules = {len(funcs)}^{len(funcs)*n} = {len(funcs)**(len(funcs)*n)}")

    # Classify each meta-rule
    results = []
    signature_counts = Counter()

    total = len(funcs) ** (len(funcs) * n)
    for i, combo in enumerate(itertools.product(range(len(funcs)),
                                                 repeat=len(funcs) * n)):
        info = classify_meta_rule(combo, funcs, n)
        sig = (info["fixed_points"], tuple(info["cycle_lengths"]),
               info["max_transient"], info["distinct_functions"])
        signature_counts[sig] += 1
        results.append(info)

        if (i + 1) % 10000 == 0:
            print(f"  Processed {i+1}/{total}...")

    print(f"\nDone. {len(results)} meta-rules classified.")
    print(f"{len(signature_counts)} distinct dynamical signatures.")

    # Sort signatures by "interestingness"
    # Interesting = long transients, many cycles, high function diversity
    sorted_sigs = sorted(signature_counts.items(),
                        key=lambda x: (x[0][2], max(x[0][1]) if x[0][1] else 0,
                                       x[0][3]),
                        reverse=True)

    print(f"\nTop 20 most interesting signatures:")
    print(f"{'Signature':<55} {'Count':>6}")
    print("-" * 62)
    for sig, count in sorted_sigs[:20]:
        fp, cl, mt, df = sig
        print(f"fp={fp}, cycles={list(cl)}, max_trans={mt}, dist_f={df}  {count:>6}")

    # Distribution of max transient lengths
    trans_dist = Counter(r["max_transient"] for r in results)
    print(f"\nMax transient distribution:")
    for t in sorted(trans_dist.keys()):
        print(f"  transient={t}: {trans_dist[t]} ({100*trans_dist[t]/len(results):.1f}%)")

    # Distribution of max cycle lengths
    cycle_dist = Counter(r["max_cycle"] for r in results)
    print(f"\nMax cycle length distribution:")
    for c in sorted(cycle_dist.keys()):
        print(f"  max_cycle={c}: {cycle_dist[c]} ({100*cycle_dist[c]/len(results):.1f}%)")

    # Distribution of distinct functions
    func_dist = Counter(r["distinct_functions"] for r in results)
    print(f"\nDistinct functions distribution:")
    for df in sorted(func_dist.keys()):
        print(f"  distinct_f={df}: {func_dist[df]} ({100*func_dist[df]/len(results):.1f}%)")

    # Find the most "creative" meta-rules
    # Score: max_transient + max_cycle + distinct_functions
    for r in results:
        r["creativity_score"] = (r["max_transient"] * 3 + r["max_cycle"] * 2
                                + r["distinct_functions"])

    top_creative = sorted(results, key=lambda r: r["creativity_score"], reverse=True)[:10]
    print(f"\nTop 10 most creative meta-rules:")
    for r in top_creative:
        print(f"  combo={r['combo']}: fp={r['fixed_points']}, "
              f"cycles={r['cycle_lengths']}, max_trans={r['max_transient']}, "
              f"dist_f={r['distinct_functions']}, score={r['creativity_score']}")

    # Save full results
    outdir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(outdir, exist_ok=True)

    summary = {
        "n": n,
        "total_meta_rules": len(results),
        "distinct_signatures": len(signature_counts),
        "transient_distribution": {str(k): v for k, v in sorted(trans_dist.items())},
        "cycle_distribution": {str(k): v for k, v in sorted(cycle_dist.items())},
        "func_diversity_distribution": {str(k): v for k, v in sorted(func_dist.items())},
        "top_signatures": [
            {"signature": {"fp": s[0], "cycles": list(s[1]),
                          "max_transient": s[2], "distinct_f": s[3]},
             "count": c}
            for s, c in sorted_sigs[:50]
        ],
        "top_creative": [
            {"combo": r["combo"], "fixed_points": r["fixed_points"],
             "cycle_lengths": r["cycle_lengths"], "max_transient": r["max_transient"],
             "distinct_functions": r["distinct_functions"],
             "creativity_score": r["creativity_score"]}
            for r in top_creative
        ],
    }

    json_path = os.path.join(outdir, "exhaustive_n2.json")
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {json_path}")


if __name__ == "__main__":
    run_exhaustive_n2()
