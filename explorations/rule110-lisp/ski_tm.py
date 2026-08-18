"""Layer 3: a Turing machine that normalizes SKI terms.

Operates on closed SKI terms in backtick (prefix) notation; performs
normal-order reduction to full normal form, reproducing ski.normalize
(differentially tested in tests/test_ski_tm.py).

Design facts:
- In prefix notation the spine backticks of a redex are string-adjacent
  (modulo skips) to the combinator, so a left-to-right finite scan for the
  first `I / ``K / ```S finds the leftmost-outermost redex.
- `I x -> x and ``K x y -> x rewrite in place; deleted characters become
  the transparent skip '_'; K's y is erased via a pebble-counter subterm
  walk (unary counter in a scratch area at the far left).
- ```S x y z -> ``x z `y z copies the current term region into a fresh
  region on the right, emitting the rearrangement on the fly. Source
  chars are blanked as consumed, so "first non-blank after $" acts as the
  source cursor. Emission order: two backticks, x(blank), y skipped
  (kept), z(kept), one backtick, y(blank), z(blank). The old region
  evaporates; '%' becomes the new '$'.

Tape layout:  # <scratch '.' cells> $ <term A> [% <term B> ^]
The harness sizes the scratch to the maximum possible subterm depth
(term length suffices).
"""

HASH, DOT, STAR = "#", ".", "*"
DOLLAR, PERCENT, CARET = "$", "%", "^"
SKIP, BLANK, LBRACK = "_", " ", "["
# f and x are inert free atoms used by the value decoder's probes
PRIME = {"`": "@", "S": "s", "K": "k", "I": "i", "f": "F", "x": "X"}
UNPRIME = {v: k for k, v in PRIME.items()}
ALPHABET = set("#.*$%^_`SKI[@skifxFX") | {BLANK}
PRIMES = tuple(PRIME.values())


class TMBuilder:
    def __init__(self):
        self.delta = {}

    def add(self, state, syms, write, move, new):
        if isinstance(syms, str):
            syms = [syms]
        for s in syms:
            key = (state, s)
            if key in self.delta:
                raise ValueError(f"duplicate transition {key}")
            self.delta[key] = (s if write is None else write, move, new)

    def default(self, state, write, move, new, except_syms=()):
        for s in ALPHABET:
            if (state, s) not in self.delta and s not in except_syms:
                self.delta[(state, s)] = (s if write is None else write,
                                          move, new)


def run_tm(delta, tape, state, halt_states, max_steps=500_000_000):
    head, n = 0, 0
    while n < max_steps:
        if state in halt_states:
            return tape, state, n
        if head >= len(tape):
            tape.extend([BLANK] * (head - len(tape) + 16))
        key = (state, tape[head])
        if key not in delta:
            raise RuntimeError(f"no transition for {key} at head {head}")
        w, mv, state = delta[key]
        tape[head] = w
        head += mv
        n += 1
        if head < 0:
            raise RuntimeError("fell off left end")
    raise RuntimeError("step budget exhausted")


# ------------------------------------------------------------- counters

def _inc(b, prefix, ret):
    b.default(f"{prefix}_inc", None, -1, f"{prefix}_inc", except_syms=("#",))
    b.add(f"{prefix}_inc", "#", None, +1, f"{prefix}_inc2")
    b.add(f"{prefix}_inc2", STAR, None, +1, f"{prefix}_inc2")
    b.add(f"{prefix}_inc2", DOT, STAR, +1, ret)


def _dec_or_done(b, prefix, ret, done_ret):
    b.default(f"{prefix}_dec", None, -1, f"{prefix}_dec", except_syms=("#",))
    b.add(f"{prefix}_dec", "#", None, +1, f"{prefix}_dec2")
    b.add(f"{prefix}_dec2", DOT, None, +1, done_ret)
    b.add(f"{prefix}_dec2", STAR, None, +1, f"{prefix}_dec3")
    b.add(f"{prefix}_dec3", STAR, None, +1, f"{prefix}_dec3")
    b.default(f"{prefix}_dec3", None, -1, f"{prefix}_dec4",
              except_syms=(STAR,))
    b.add(f"{prefix}_dec4", STAR, DOT, +1, ret)


def _walk_right_to_prime(b, state, out):
    """out(state, primed_char, original)"""
    b.default(state, None, +1, state, except_syms=PRIMES)
    for pc, orig in UNPRIME.items():
        out(state, pc, orig)


def _counter_walk(b, prefix, erase, then):
    """Head at first char of a subterm (skips allowed): traverse exactly
    one subterm; erase to '_' if erase; end one past it in state `then`."""
    st = f"{prefix}_init"
    b.add(st, [SKIP, BLANK], None, +1, st)
    b.add(st, "`", PRIME["`"], -1, f"{prefix}_inc")
    for c in "SKIfx":
        b.add(st, c, PRIME[c], -1, f"{prefix}_dec")
    _inc(b, prefix, f"{prefix}_ret")
    _dec_or_done(b, prefix, f"{prefix}_ret", f"{prefix}_doneret")
    for state in (f"{prefix}_ret", f"{prefix}_doneret"):
        done = state.endswith("_doneret")
        def out(stt, pc, orig, done=done):
            b.add(stt, pc, SKIP if erase else orig, +1,
                  then if done else st)
        _walk_right_to_prime(b, state, out)


def _counter_copy(b, prefix, blank_src, then):
    """Head at (or before, over skips/blanks) the first char of a subterm:
    copy it char-by-char to the frontier '^'. Source chars become BLANK if
    blank_src else stay. Ends one past the subterm in state `then`."""
    st = f"{prefix}_init"
    b.add(st, [SKIP, BLANK], None, +1, st)     # skips are dropped, not copied
    b.add(st, "`", PRIME["`"], -1, f"{prefix}_inc")
    for c in "SKIfx":
        b.add(st, c, PRIME[c], -1, f"{prefix}_dec")
    _inc(b, prefix, f"{prefix}_ret")
    _dec_or_done(b, prefix, f"{prefix}_ret", f"{prefix}_doneret")
    # after the counter trip, walk right to the prime, KEEP it primed,
    # and continue right to the frontier to emit its char.
    for state in (f"{prefix}_ret", f"{prefix}_doneret"):
        tag = "d" if state.endswith("_doneret") else "c"
        def out(stt, pc, orig, tag=tag):
            b.add(stt, pc, None, +1, f"{prefix}{tag}_go_{PRIME[orig]}")
        _walk_right_to_prime(b, state, out)
    for tag, nxt in (("c", st), ("d", then)):
        for pc, orig in UNPRIME.items():
            go = f"{prefix}{tag}_go_{pc}"
            b.default(go, None, +1, go, except_syms=(CARET,))
            b.add(go, CARET, orig, +1, f"{prefix}{tag}_put_{pc}")
        for pc in UNPRIME:
            b.add(f"{prefix}{tag}_put_{pc}", BLANK, CARET, -1,
                  f"{prefix}{tag}_back_{pc}")
            back = f"{prefix}{tag}_back_{pc}"
            b.default(back, None, -1, back, except_syms=(pc,))
            b.add(back, pc, BLANK if blank_src else UNPRIME[pc], +1, nxt)


def _emit_lit(b, prefix, ch, then):
    """Walk right to '^', write ch, advance '^', then walk left to '$' and
    enter `then` (which should walk right from $)."""
    st = f"{prefix}_go"
    b.default(st, None, +1, st, except_syms=(CARET,))
    b.add(st, CARET, ch, +1, f"{prefix}_put")
    b.add(f"{prefix}_put", BLANK, CARET, -1, f"{prefix}_back")
    b.default(f"{prefix}_back", None, -1, f"{prefix}_back",
              except_syms=(DOLLAR,))
    b.add(f"{prefix}_back", DOLLAR, None, +1, then)


def build_machine():
    b = TMBuilder()

    # phase 1: find $ then scan for a redex
    b.add("start", "#", None, +1, "seek$")
    b.default("seek$", None, +1, "seek$", except_syms=(DOLLAR,))
    b.add("seek$", DOLLAR, None, +1, "scan0")
    for k in range(4):
        st = f"scan{k}"
        b.add(st, SKIP, None, +1, st)
        b.add(st, "`", None, +1, f"scan{min(k + 1, 3)}")
        b.add(st, [BLANK, CARET], None, 0, "DONE")
        b.add(st, "I", ("_" if k >= 1 else "I"), (-1 if k >= 1 else +1),
              ("delI" if k >= 1 else "scan0"))
        b.add(st, "K", ("_" if k >= 2 else "K"), (-1 if k >= 2 else +1),
              ("delK1" if k >= 2 else "scan0"))
        b.add(st, "S", ("_" if k >= 3 else "S"), (-1 if k >= 3 else +1),
              ("sm1" if k >= 3 else "scan0"))
        b.add(st, ["f", "x"], None, +1, "scan0")   # inert atoms

    # I redex: delete the ` to the left
    b.add("delI", SKIP, None, -1, "delI")
    b.add("delI", "`", SKIP, +1, "rescan")
    # K redex: delete two `s, skip x, erase y
    b.add("delK1", SKIP, None, -1, "delK1")
    b.add("delK1", "`", SKIP, -1, "delK2")
    b.add("delK2", SKIP, None, -1, "delK2")
    b.add("delK2", "`", SKIP, +1, "kx_init")
    _counter_walk(b, "kx", erase=False, then="ky_init")
    _counter_walk(b, "ky", erase=True, then="rescan")

    b.default("rescan", None, -1, "rescan", except_syms=("#",))
    b.add("rescan", "#", None, +1, "seek$")

    # S redex: blank the S (done by scan3), blank inner two `s, mark the
    # outermost ` as '[' , then set up % and ^ at the term end
    b.add("sm1", SKIP, None, -1, "sm1")
    b.add("sm1", "`", SKIP, -1, "sm2")
    b.add("sm2", SKIP, None, -1, "sm2")
    b.add("sm2", "`", SKIP, -1, "sm3")
    b.add("sm3", SKIP, None, -1, "sm3")
    b.add("sm3", "`", LBRACK, +1, "sm_end")
    # walk right to term end (BLANK, or ^ from a previous round)
    b.default("sm_end", None, +1, "sm_end", except_syms=(BLANK, CARET))
    b.add("sm_end", [BLANK, CARET], PERCENT, +1, "sm_caret")
    b.add("sm_caret", BLANK, CARET, -1, "sm_back")
    b.default("sm_back", None, -1, "sm_back", except_syms=(DOLLAR,))
    b.add("sm_back", DOLLAR, None, +1, "copy")

    # main copy loop: from $, first non-blank char decides
    b.add("copy", [BLANK, SKIP], None, +1, "copy")
    b.add("copy", LBRACK, BLANK, 0, "sredex0_go")
    for c in "`SKIfx":
        b.add("copy", c, PRIME[c], +1, f"copyc_go_{PRIME[c]}")
    b.add("copy", PERCENT, DOLLAR, -1, "fin")
    # plain char: emit at frontier, blank source, loop
    for pc, orig in UNPRIME.items():
        go = f"copyc_go_{pc}"
        b.default(go, None, +1, go, except_syms=(CARET,))
        b.add(go, CARET, orig, +1, f"copyc_put_{pc}")
        b.add(f"copyc_put_{pc}", BLANK, CARET, -1, f"copyc_back_{pc}")
        back = f"copyc_back_{pc}"
        b.default(back, None, -1, back, except_syms=(pc,))
        b.add(back, pc, BLANK, +1, "copy")
    # S-redex dance: emit ``, copy x, skip y, copy z (keep), emit `,
    # copy y (blank), copy z (blank), back to main loop
    _emit_lit(b, "sredex0", "`", "sredex1_seek")
    b.add("sredex1_seek", [BLANK, SKIP], None, +1, "sredex1_seek")
    b.default("sredex1_seek", None, 0, "sredex1b_go",
              except_syms=(BLANK, SKIP))
    _emit_lit(b, "sredex1b", "`", "sx_seek")
    b.add("sx_seek", [BLANK, SKIP], None, +1, "sx_seek")
    b.default("sx_seek", None, 0, "sx_init", except_syms=(BLANK, SKIP))
    _counter_copy(b, "sx", blank_src=True, then="syskip_init")
    _counter_walk(b, "syskip", erase=False, then="sz1_init")
    _counter_copy(b, "sz1", blank_src=False, then="smid_go")
    _emit_lit(b, "smid", "`", "sy2_seek")
    b.add("sy2_seek", [BLANK, SKIP], None, +1, "sy2_seek")
    b.default("sy2_seek", None, 0, "sy2_init", except_syms=(BLANK, SKIP))
    _counter_copy(b, "sy2", blank_src=True, then="sz2_init")
    _counter_copy(b, "sz2", blank_src=True, then="copy")
    # finish: % became the new $; blank the old $ to the left, rescan
    b.default("fin", None, -1, "fin", except_syms=(DOLLAR,))
    b.add("fin", DOLLAR, BLANK, -1, "rescan")
    return b


def normalize_tm(term, max_steps=500_000_000):
    """Run the machine on a closed SKI term; return (normal form, steps)."""
    b = build_machine()
    scratch = len(term) + 4
    tape = list("#" + "." * scratch + "$" + term)
    tape, state, steps = run_tm(b.delta, tape, "start", {"DONE"}, max_steps)
    s = "".join(tape)
    start = s.rindex("$") + 1
    out = "".join(c for c in s[start:] if c in "`SKIfx")
    return out, steps
