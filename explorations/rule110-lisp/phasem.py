"""Phase machines: a cyclic tag system viewed one symbol (not one bit) at a time.

A phase machine has letters 0..B-1 (B a multiple of 6) plus a blank, and
m phases. Letter i is the CTS word N^i Y N^(B-1-i); the blank is N^B. The
CTS has p = m*B appendants. Because every appendant is a whole number of
B-bit words, symbol boundaries stay on multiples of B, and the symbol at
absolute symbol index k is always read with phase k mod m.

Semantics (exactly the CTS's, grouped by symbols):
  read the front symbol; at phase f a letter c appends rules[f][c] (a
  nonempty tuple of letters and BLANKs); a blank appends nothing.

Why rules may not be empty: Cook's glider construction fails on empty
appendants (REPORT.md 3.4); a phase machine never needs them, because a
letter that should vanish can become a blank, which then vanishes.
Unused (phase, letter) pairs get a single blank, and run() raises if one
is ever read, so a program cannot silently depend on it.

What a symbol "knows" when read: its letter and its phase. The phase of a
symbol is fixed when it is appended: it is the queue's absolute length at
that time mod m. So every append "samples" a global quantity, and a
symbol that emits extra blanks shifts the phase of everything appended
after it. This is the only way information moves between symbols
(INTERPRETER.md section 2).
"""

from collections import deque

BLANK = -1
UNUSED = "N" * 6           # appendant of a (phase, letter) that never fires


class PhaseMachine:
    def __init__(self, B, m, rules):
        """rules: dict (phase, letter) -> tuple of letters/BLANK (nonempty).
        Missing pairs are 'never read'."""
        if B % 6:
            raise ValueError(f"B={B} must be a multiple of 6 (Cook)")
        self.B, self.m = B, m
        self.rules = {}
        for (f, c), word in rules.items():
            if not (0 <= f < m and 0 <= c < B):
                raise ValueError(f"bad rule key {(f, c)}")
            word = tuple(word)
            if not word:
                raise ValueError(f"rule {(f, c)} is empty")
            if any(x != BLANK and not 0 <= x < B for x in word):
                raise ValueError(f"rule {(f, c)} has a bad letter: {word}")
            self.rules[(f, c)] = word

    # ---- symbol-level run -------------------------------------------------
    def run(self, tape, max_reads, on_read=None):
        """Run from `tape` (letters/BLANK; tape[0] has phase 0). Returns
        (queue, reads) where queue holds (letter, phase) pairs. Stops when
        the queue empties or after max_reads symbol reads. on_read(k, c, f)
        is called before each read of a letter (not of blanks)."""
        q = deque((c, k % self.m) for k, c in enumerate(tape))
        nxt = len(tape)                   # absolute index of the next append
        for k in range(max_reads):
            if not q:
                return q, k
            c, f = q.popleft()
            if c == BLANK:
                continue
            if on_read is not None:
                on_read(k, c, f)
            word = self.rules.get((f, c))
            if word is None:
                raise RuntimeError(f"read letter {c} at phase {f}: no rule")
            for x in word:
                q.append((x, nxt % self.m))
                nxt += 1
        return q, max_reads

    # ---- CTS compilation --------------------------------------------------
    def letter_word(self, c):
        if c == BLANK:
            return "N" * self.B
        return "N" * c + "Y" + "N" * (self.B - 1 - c)

    def encode(self, tape):
        return "".join(self.letter_word(c) for c in tape)

    def appendants(self):
        """CTS appendant list, index f*B + c. A pair with no rule is never
        read as Y (run() raises if its letter is read), so its appendant is
        never appended; it only has to be nonempty with a length that is a
        multiple of 6 (Cook), and the shortest, N^6, keeps the table short."""
        out = []
        for f in range(self.m):
            for c in range(self.B):
                word = self.rules.get((f, c))
                out.append(UNUSED if word is None else
                           "".join(self.letter_word(x) for x in word))
        return out

    def decode(self, cts_tape, start):
        """CTS tape (string) whose first bit has absolute index `start`
        (a multiple of B) -> list of (letter, phase)."""
        if start % self.B or len(cts_tape) % self.B:
            raise ValueError("CTS tape not aligned to symbols")
        out = []
        for i in range(0, len(cts_tape), self.B):
            w = cts_tape[i:i + self.B]
            n = w.count("Y")
            if n > 1:
                raise ValueError(f"symbol word {w} has {n} Y's")
            c = w.index("Y") if n else BLANK
            out.append((c, ((start + i) // self.B) % self.m))
        return out
