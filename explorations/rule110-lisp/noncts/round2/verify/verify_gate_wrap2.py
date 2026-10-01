"""Differential test of gate's {I, N, Z} stream against the abstract model
I: v+1, N: v, Z: v-1 if v > 0 else 6  (a mod-7 down/up counter).
Random words, gate's placement rule, my translation/evolution/typer."""
import random, sys
import vlib, xlate, gate_scene

def ca(word):
    sc = gate_scene.scene(list(word))
    ex = xlate.expand(sc)
    items, c0 = xlate.translate(ex)
    T = int(15 * (items[-1][2] + 200)) + 2000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    assert [p[2] for p in placed] == [i[2] for i in items]
    r = vlib.evolve(row, T)
    return [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]

def model(word):
    v = 0
    for c in word:
        v = v + 1 if c == "I" else v if c == "N" else (v - 1 if v > 0 else 6)
    return ["E" if v == 0 else f"E^{v+1}"]

def main():
  rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
  n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
  fails = 0
  for i in range(n):
      L = rng.randint(3, 9)
      w = "".join(rng.choice("IIZZN") for _ in range(L))
      got, exp = ca(w), model(w)
      fails += got != exp
      print(w, got, exp, "OK" if got == exp else "MISMATCH", flush=True)
  print(f"{n} words, {fails} mismatches")


if __name__ == "__main__":
    main()
