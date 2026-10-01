"""Lower bound on the left speed of influence inside the E^n rod interior
(background tile 1101011100, period: 5 steps, shift 2 mod 10).

All 2^w perturbations of a w-cell window, at every bg time phase (0..4) and
every window alignment (0..9), evolved T steps with an independent numpy
Rule 110 stepper; record the leftmost cell differing from the unperturbed
bg evolution. Prints, per T, the maximum leftward displacement of the
influence edge (relative to the window's left end) and the pattern."""
import sys
import numpy as np

TILE = np.array([int(c) for c in "1101011100"], np.uint8)


def step(a):                       # a: (k, n); fixed edges are irrelevant (margins)
    l = np.empty_like(a); r = np.empty_like(a)
    l[:, 1:] = a[:, :-1]; l[:, 0] = a[:, 0]
    r[:, :-1] = a[:, 1:]; r[:, -1] = a[:, -1]
    return (a | r) & (1 - (l & a & r))


def run(w, T):
    best = {}
    n = w + 2 * T + 20
    a0 = T + 10                    # window start index
    pats = ((np.arange(2 ** w)[:, None] >> np.arange(w)) & 1).astype(np.uint8)
    for ph in range(5):
        for al in range(10):
            bg = TILE[(np.arange(n) + al) % 10][None, :]
            for _ in range(ph):
                bg = step(np.repeat(bg, 1, 0))
            cur = np.repeat(bg, 2 ** w, 0)
            cur[:, a0:a0 + w] = pats
            ref = bg.copy()
            for t in range(1, T + 1):
                cur = step(cur); ref = step(ref)
                d = cur != ref
                any_ = d.any(1)
                first = np.where(any_, d.argmax(1), n)
                disp = a0 - first.min()
                k = int(first.argmin())
                if disp > best.get(t, (-99,))[0]:
                    best[t] = (int(disp), ph, al, "".join(map(str, pats[k])))
    return best


if __name__ == "__main__":
    w, T = int(sys.argv[1]), int(sys.argv[2])
    best = run(w, T)
    for t in sorted(best):
        print(t, best[t], f"speed {best[t][0] / t:.3f}")
