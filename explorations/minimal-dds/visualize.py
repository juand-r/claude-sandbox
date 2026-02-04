"""
Visualization for Minimal DDS.

Generates:
1. Functional graph (all states, edges show transitions)
2. Summary statistics across meta-rules
3. Orbit complexity measures
"""

import json
import os
from collections import Counter
from dds import (
    Func, State, MetaRule, OrbitInfo, SystemAnalysis,
    enumerate_functions, analyze_system, analyze_orbit, step,
    identity_meta, make_shift_table_meta, make_xor_output_meta,
    make_permute_table_meta, make_rotate_meta,
)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("Warning: matplotlib not available, skipping plots")

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False
    print("Warning: networkx not available, skipping graph plots")


def build_functional_graph(n: int, phi: MetaRule) -> dict[tuple, tuple]:
    """Build the functional graph as a dict: state -> next_state.
    States are represented as (func_table, x) tuples for hashability.
    """
    funcs = enumerate_functions(n)
    graph = {}
    for f in funcs:
        for x in range(n):
            s = State(f, x)
            s_next = step(s, phi)
            graph[(f.table, x)] = (s_next.f.table, s_next.x)
    return graph


def classify_components(graph: dict[tuple, tuple]) -> dict:
    """Classify the functional graph into connected components with cycles."""
    # Find all cycles using Floyd's or by following edges
    visited = {}
    components = []
    node_to_component = {}

    for start in graph:
        if start in visited:
            continue

        # Follow the path from start
        path = []
        path_set = {}
        node = start
        while node not in visited and node not in path_set:
            path_set[node] = len(path)
            path.append(node)
            node = graph[node]

        if node in path_set:
            # Found a new cycle
            cycle_start_idx = path_set[node]
            cycle = path[cycle_start_idx:]
            tail = path[:cycle_start_idx]

            comp_id = len(components)
            components.append({
                "cycle": cycle,
                "cycle_length": len(cycle),
                "tail_nodes": list(tail),
            })
            for n_ in path:
                visited[n_] = comp_id
                node_to_component[n_] = comp_id
        else:
            # Reached a node already visited (in an existing component)
            comp_id = visited[node]
            for n_ in path:
                visited[n_] = comp_id
                node_to_component[n_] = comp_id

    return {
        "components": components,
        "node_to_component": node_to_component,
    }


def lempel_ziv_complexity(sequence: list) -> int:
    """Lempel-Ziv complexity: count the number of distinct substrings
    encountered when scanning left to right. Higher = more complex."""
    s = [str(x) for x in sequence]
    n = len(s)
    if n == 0:
        return 0

    complexity = 1
    i = 0
    k = 1
    kmax = 1

    while i + k <= n:
        # Check if s[i+1:i+k+1] appears in s[0:i+k]
        substr = ''.join(s[i+1:i+k+1]) if i + k + 1 <= n else None
        prefix = ''.join(s[0:i+k])
        if substr and substr in prefix:
            k += 1
            if k > kmax:
                kmax = k
        else:
            complexity += 1
            i += kmax
            k = 1
            kmax = 1

    return complexity


def orbit_complexity_measures(info: OrbitInfo) -> dict:
    """Compute various complexity measures for an orbit."""
    traj = info.trajectory

    # Sequence of x values
    x_seq = [s.x for s in traj]
    # Sequence of function indices (as tuples for hashing)
    f_seq = [s.f.table for s in traj]

    # LZ complexity of x sequence
    lz_x = lempel_ziv_complexity(x_seq)

    # LZ complexity of function sequence
    lz_f = lempel_ziv_complexity(f_seq)

    # Function mutation rate: fraction of steps where f changes
    f_changes = sum(1 for i in range(1, len(traj)) if traj[i].f != traj[i-1].f)
    mutation_rate = f_changes / max(len(traj) - 1, 1)

    # "Creativity score": combination of transient length, distinct states,
    # and mutation rate. Higher = more "creative" dynamics.
    creativity = (
        info.transient_length
        + info.distinct_functions
        + info.distinct_x_values
        + lz_x + lz_f
    )

    return {
        "lz_x": lz_x,
        "lz_f": lz_f,
        "mutation_rate": round(mutation_rate, 3),
        "creativity_score": creativity,
    }


def plot_functional_graph(n: int, phi: MetaRule, phi_name: str, outdir: str):
    """Plot the functional graph using networkx + matplotlib."""
    if not HAS_NX or not HAS_MPL:
        return

    graph = build_functional_graph(n, phi)

    G = nx.DiGraph()
    for src, dst in graph.items():
        # Label: F[table]_x
        src_label = f"F{list(src[0])}_{src[1]}"
        dst_label = f"F{list(dst[0])}_{dst[1]}"
        G.add_edge(src_label, dst_label)

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    # Use spring layout
    pos = nx.spring_layout(G, seed=42, k=2.0 / (len(G.nodes()) ** 0.5))

    # Color nodes by in-degree (attractors have higher in-degree)
    in_degrees = dict(G.in_degree())
    node_colors = [in_degrees[n_] for n_ in G.nodes()]

    nx.draw(G, pos, ax=ax,
            node_size=300,
            node_color=node_colors,
            cmap=plt.cm.YlOrRd,
            with_labels=True,
            font_size=5,
            arrows=True,
            arrowsize=10,
            edge_color='gray',
            alpha=0.9)

    ax.set_title(f"Functional Graph: n={n}, phi={phi_name}\n"
                 f"|States| = {len(G.nodes())}")

    outpath = os.path.join(outdir, f"functional_graph_n{n}_{phi_name}.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {outpath}")


def plot_comparison(n: int, results: list[dict], outdir: str):
    """Bar chart comparing meta-rules."""
    if not HAS_MPL:
        return

    names = [r["phi"] for r in results]
    metrics = ["fixed_points", "distinct_cycles", "max_transient",
               "max_cycle_length", "avg_distinct_functions"]

    fig, axes = plt.subplots(1, len(metrics), figsize=(4 * len(metrics), 4))

    for i, metric in enumerate(metrics):
        values = [r[metric] for r in results]
        axes[i].bar(range(len(names)), values, color=plt.cm.Set2(range(len(names))))
        axes[i].set_xticks(range(len(names)))
        axes[i].set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        axes[i].set_title(metric.replace('_', ' '), fontsize=10)

    fig.suptitle(f"Meta-rule Comparison (n={n})", fontsize=14)
    plt.tight_layout()

    outpath = os.path.join(outdir, f"comparison_n{n}.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {outpath}")


def plot_orbit_complexity(n: int, analyses: list[tuple[str, SystemAnalysis]], outdir: str):
    """Scatter plot of orbit properties across meta-rules."""
    if not HAS_MPL:
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for phi_name, analysis in analyses:
        transients = []
        cycles = []
        mutation_rates = []
        creativity_scores = []

        for orb in analysis.orbits:
            cm = orbit_complexity_measures(orb)
            transients.append(orb.transient_length)
            cycles.append(orb.cycle_length)
            mutation_rates.append(cm["mutation_rate"])
            creativity_scores.append(cm["creativity_score"])

        axes[0].scatter(transients, cycles, alpha=0.5, s=20, label=phi_name)
        axes[1].scatter(transients, mutation_rates, alpha=0.5, s=20, label=phi_name)
        axes[2].scatter(mutation_rates, creativity_scores, alpha=0.5, s=20, label=phi_name)

    axes[0].set_xlabel("Transient length")
    axes[0].set_ylabel("Cycle length")
    axes[0].set_title("Transient vs Cycle")
    axes[0].legend(fontsize=7)

    axes[1].set_xlabel("Transient length")
    axes[1].set_ylabel("Mutation rate")
    axes[1].set_title("Transient vs Mutation")
    axes[1].legend(fontsize=7)

    axes[2].set_xlabel("Mutation rate")
    axes[2].set_ylabel("Creativity score")
    axes[2].set_title("Mutation vs Creativity")
    axes[2].legend(fontsize=7)

    fig.suptitle(f"Orbit Complexity (n={n})", fontsize=14)
    plt.tight_layout()

    outpath = os.path.join(outdir, f"orbit_complexity_n{n}.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {outpath}")


def run_full_analysis(n: int, outdir: str):
    """Run complete analysis for a given n."""
    os.makedirs(outdir, exist_ok=True)

    meta_rules = [
        ("identity", identity_meta),
        ("shift_table", make_shift_table_meta()),
        ("xor_output", make_xor_output_meta(n)),
    ]

    # Add permute_table for n=2: swap positions
    if n == 2:
        meta_rules.append(("permute_01", make_permute_table_meta((1, 0))))

    # Add rotate through first few functions
    funcs = enumerate_functions(n)
    if len(funcs) >= 3:
        meta_rules.append(("rotate_3", make_rotate_meta(funcs[:3])))

    print(f"\n{'='*60}")
    print(f"Full analysis for n={n}")
    print(f"  |X| = {n}, |F| = {n**n}, |States| = {n**n * n}")
    print(f"  Meta-rules: {[name for name, _ in meta_rules]}")
    print(f"{'='*60}")

    summaries = []
    analyses = []

    for name, phi in meta_rules:
        print(f"\n  Analyzing: {name}...")
        analysis = analyze_system(n, phi, name)
        s = analysis.summary()
        summaries.append(s)
        analyses.append((name, analysis))

        print(f"    Fixed points: {s['fixed_points']}")
        print(f"    Distinct cycles: {s['distinct_cycles']}")
        print(f"    Max transient: {s['max_transient']}")
        print(f"    Max cycle: {s['max_cycle_length']}")
        print(f"    Avg distinct functions: {s['avg_distinct_functions']}")

        # Compute complexity for most interesting orbits
        interesting = sorted(analysis.orbits,
                           key=lambda o: o.transient_length + o.cycle_length,
                           reverse=True)[:3]
        for orb in interesting:
            cm = orbit_complexity_measures(orb)
            print(f"    Top orbit: {orb.initial} -> trans={orb.transient_length}, "
                  f"cycle={orb.cycle_length}, mutation={cm['mutation_rate']}, "
                  f"creativity={cm['creativity_score']}")

    # Save summaries as JSON
    json_path = os.path.join(outdir, f"summary_n{n}.json")
    with open(json_path, 'w') as f:
        json.dump(summaries, f, indent=2)
    print(f"\n  Saved: {json_path}")

    # Generate plots
    print("\n  Generating plots...")
    for name, phi in meta_rules:
        plot_functional_graph(n, phi, name, outdir)

    plot_comparison(n, summaries, outdir)
    plot_orbit_complexity(n, analyses, outdir)


if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "results")
    run_full_analysis(2, outdir)
    run_full_analysis(3, outdir)
