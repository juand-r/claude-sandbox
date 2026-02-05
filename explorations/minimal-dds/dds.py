"""
Minimal Discrete Dynamical Systems on (Function, Input) pairs.

State = (f, x) where f: X -> X and x in X.
Transition: (f, x) -> (phi(f, x), f(x))

phi is the "meta-rule" that updates the function.
When phi is identity, this is ordinary iteration of a fixed f.
When phi is nontrivial, the system rewrites its own rules.

We work with small finite X = {0, 1, ..., n-1} so that
F = X^X has n^n elements. This lets us enumerate everything.
"""

import itertools
from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Func:
    """A function X -> X represented as a tuple of values.
    For X = {0, ..., n-1}, table[i] = f(i).
    """
    table: tuple[int, ...]

    def __call__(self, x: int) -> int:
        return self.table[x]

    @property
    def n(self) -> int:
        return len(self.table)

    def __repr__(self):
        return f"F{list(self.table)}"


@dataclass(frozen=True)
class State:
    """A state (f, x) in the dynamical system."""
    f: Func
    x: int

    def __repr__(self):
        return f"({self.f}, {self.x})"


def enumerate_functions(n: int) -> list[Func]:
    """All functions X -> X where X = {0, ..., n-1}. There are n^n of them."""
    return [Func(table) for table in itertools.product(range(n), repeat=n)]


MetaRule = Callable[[Func, int], Func]


def identity_meta(_f: Func, _x: int) -> Func:
    """Meta-rule that never changes the function."""
    return _f


def step(state: State, phi: MetaRule) -> State:
    """One step of the dynamical system: (f, x) -> (phi(f, x), f(x))."""
    new_f = phi(state.f, state.x)
    new_x = state.f(state.x)
    return State(new_f, new_x)


def orbit(state: State, phi: MetaRule, max_steps: int = 1000) -> list[State]:
    """Compute the orbit of a state until it revisits a state or hits max_steps."""
    visited = {}
    trajectory = []
    s = state
    for i in range(max_steps):
        if s in visited:
            return trajectory
        visited[s] = i
        trajectory.append(s)
        s = step(s, phi)
    trajectory.append(s)  # include the max_steps state
    return trajectory


@dataclass
class OrbitInfo:
    """Analysis of an orbit."""
    initial: State
    transient_length: int  # steps before entering cycle
    cycle_length: int      # length of the cycle (0 if max_steps hit)
    trajectory: list[State]
    # How many distinct functions appear in the orbit
    distinct_functions: int
    # How many distinct x values appear
    distinct_x_values: int

    @property
    def total_length(self) -> int:
        return self.transient_length + self.cycle_length


def analyze_orbit(state: State, phi: MetaRule, max_steps: int = 1000) -> OrbitInfo:
    """Compute orbit and classify it."""
    visited = {}
    trajectory = []
    s = state
    for i in range(max_steps):
        if s in visited:
            transient = visited[s]
            cycle = i - transient
            funcs = {t.f for t in trajectory}
            xs = {t.x for t in trajectory}
            return OrbitInfo(
                initial=state,
                transient_length=transient,
                cycle_length=cycle,
                trajectory=trajectory,
                distinct_functions=len(funcs),
                distinct_x_values=len(xs),
            )
        visited[s] = i
        trajectory.append(s)
        s = step(s, phi)

    funcs = {t.f for t in trajectory}
    xs = {t.x for t in trajectory}
    return OrbitInfo(
        initial=state,
        transient_length=len(trajectory),
        cycle_length=0,
        trajectory=trajectory,
        distinct_functions=len(funcs),
        distinct_x_values=len(xs),
    )


@dataclass
class SystemAnalysis:
    """Full analysis of a dynamical system (all initial states, one meta-rule)."""
    n: int
    phi_name: str
    orbits: list[OrbitInfo] = field(default_factory=list)

    @property
    def num_fixed_points(self) -> int:
        return sum(1 for o in self.orbits if o.cycle_length == 1 and o.transient_length == 0)

    @property
    def num_cycles(self) -> int:
        """Number of distinct cycles (not counting fixed points)."""
        cycles = set()
        for o in self.orbits:
            if o.cycle_length > 1:
                # Identify cycle by its lexicographically smallest state
                cycle_states = o.trajectory[o.transient_length:]
                min_state = min(cycle_states, key=lambda s: (s.f.table, s.x))
                cycles.add((min_state.f.table, min_state.x, o.cycle_length))
        return len(cycles)

    @property
    def max_transient(self) -> int:
        return max((o.transient_length for o in self.orbits), default=0)

    @property
    def max_cycle_length(self) -> int:
        return max((o.cycle_length for o in self.orbits), default=0)

    @property
    def avg_distinct_functions(self) -> float:
        if not self.orbits:
            return 0.0
        return sum(o.distinct_functions for o in self.orbits) / len(self.orbits)

    def summary(self) -> dict:
        return {
            "n": self.n,
            "phi": self.phi_name,
            "total_states": len(self.orbits),
            "fixed_points": self.num_fixed_points,
            "distinct_cycles": self.num_cycles,
            "max_transient": self.max_transient,
            "max_cycle_length": self.max_cycle_length,
            "avg_distinct_functions": round(self.avg_distinct_functions, 2),
        }


def analyze_system(n: int, phi: MetaRule, phi_name: str = "unknown") -> SystemAnalysis:
    """Analyze the full dynamical system for all initial states (f, x)."""
    funcs = enumerate_functions(n)
    analysis = SystemAnalysis(n=n, phi_name=phi_name)

    for f in funcs:
        for x in range(n):
            state = State(f, x)
            info = analyze_orbit(state, phi)
            analysis.orbits.append(info)

    return analysis


# --- Built-in meta-rules ---

def make_constant_meta(target_func: Func) -> MetaRule:
    """Always switch to a fixed target function."""
    def phi(_f: Func, _x: int) -> Func:
        return target_func
    return phi


def make_output_dependent_meta(func_map: dict[int, Func]) -> MetaRule:
    """Next function depends only on current output f(x).
    func_map: {output_value: next_function}
    """
    def phi(f: Func, x: int) -> Func:
        output = f(x)
        return func_map[output]
    return phi


def make_rotate_meta(funcs: list[Func]) -> MetaRule:
    """Cycle through a list of functions regardless of state."""
    func_index = {}
    for i, f in enumerate(funcs):
        func_index[f.table] = i

    def phi(f: Func, _x: int) -> Func:
        idx = func_index.get(f.table, 0)
        return funcs[(idx + 1) % len(funcs)]
    return phi


def make_permute_table_meta(perm: tuple[int, ...]) -> MetaRule:
    """Apply a permutation to the function's output table.
    perm[i] = j means position i of new table gets value from position j of old table.
    """
    def phi(f: Func, _x: int) -> Func:
        new_table = tuple(f.table[perm[i]] for i in range(f.n))
        return Func(new_table)
    return phi


def make_shift_table_meta() -> MetaRule:
    """Shift the function table left by one (circular)."""
    def phi(f: Func, _x: int) -> Func:
        return Func(f.table[1:] + (f.table[0],))
    return phi


def make_xor_output_meta(n: int) -> MetaRule:
    """XOR each table entry with the current input x (for binary/small n)."""
    def phi(f: Func, x: int) -> Func:
        new_table = tuple((v + x) % n for v in f.table)
        return Func(new_table)
    return phi


if __name__ == "__main__":
    # Quick demo with n=2
    n = 2
    print(f"=== Discrete Dynamical System on (F, X) with |X| = {n} ===")
    print(f"|F| = {n}^{n} = {n**n}")
    print(f"Total states |F x X| = {n**n * n}")
    print()

    # Test with identity meta-rule (ordinary iteration)
    print("--- Meta-rule: identity (ordinary iteration) ---")
    analysis = analyze_system(n, identity_meta, "identity")
    for k, v in analysis.summary().items():
        print(f"  {k}: {v}")
    print()

    # Test with shift-table meta-rule
    print("--- Meta-rule: shift table ---")
    analysis = analyze_system(n, make_shift_table_meta(), "shift_table")
    for k, v in analysis.summary().items():
        print(f"  {k}: {v}")
    print()

    # Test with xor-output meta-rule
    print("--- Meta-rule: xor output (mod n) ---")
    analysis = analyze_system(n, make_xor_output_meta(n), "xor_output")
    for k, v in analysis.summary().items():
        print(f"  {k}: {v}")
    print()

    # Show some example orbits for the xor_output meta-rule
    print("--- Example orbits (xor_output, n=2) ---")
    phi = make_xor_output_meta(n)
    funcs = enumerate_functions(n)
    for f in funcs[:4]:
        for x in range(n):
            info = analyze_orbit(State(f, x), phi)
            traj_str = " -> ".join(str(s) for s in info.trajectory[:8])
            if len(info.trajectory) > 8:
                traj_str += " -> ..."
            print(f"  {info.initial}: transient={info.transient_length}, "
                  f"cycle={info.cycle_length}, distinct_f={info.distinct_functions}")
            print(f"    {traj_str}")
    print()

    # n=3 summary
    n = 3
    print(f"=== n = {n}: |F| = {n**n}, total states = {n**n * n} ===")
    for name, phi in [
        ("identity", identity_meta),
        ("shift_table", make_shift_table_meta()),
        ("xor_output", make_xor_output_meta(n)),
    ]:
        analysis = analyze_system(n, phi, name)
        s = analysis.summary()
        print(f"  {name}: fixed={s['fixed_points']}, cycles={s['distinct_cycles']}, "
              f"max_trans={s['max_transient']}, max_cycle={s['max_cycle_length']}, "
              f"avg_funcs={s['avg_distinct_functions']}")
