"""Spatial rock-paper-scissors with MOBILITY (Reichenbach-Mobilia-Frey 2007).

The canonical model that produces rotating spiral waves, which the ring
system's in-place-overwrite RPS (E16/E17) could not. Three reactions on a
torus, each applied to a random adjacent pair:
  selection    : predator kills prey  (prey site -> empty)
  reproduction : occupied -> fills an empty neighbour
  exchange     : two neighbours swap   (this is the mobility that makes spirals)
States: 0 empty, 1/2/3 species; cyclic dominance a beats b iff (a-b)%3==2.

Run: python3 spiral_rps.py  (writes out/spiral.gif and out/_spiral_last.png)
"""
import numpy as np, time
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib.colors import ListedColormap

def run(side=128, gens=500, pe=0.1, seed=1, render=True, out="out/spiral"):
    rng = np.random.default_rng(seed); n = side*side
    S = rng.integers(0, 4, size=n).astype(np.int8)     # 0 empty, 1/2/3
    cmap = ListedColormap(['#111','#e0443a','#3ab04a','#3a6fe0'])
    def gen():
        sites = rng.integers(0, n, size=n)
        dirs = rng.integers(0, 4, size=n)
        react = rng.random(n)
        for k in range(n):
            p = int(sites[k]); x = p % side; y = p // side; d = dirs[k]
            if   d == 0: q = ((y-1) % side)*side + x
            elif d == 1: q = ((y+1) % side)*side + x
            elif d == 2: q = y*side + (x-1) % side
            else:        q = y*side + (x+1) % side
            a = S[p]; b = S[q]
            if react[k] < pe:                     # exchange (mobility)
                S[p] = b; S[q] = a
            elif a and b:                         # selection
                if (a-b) % 3 == 2: S[q] = 0
                elif (b-a) % 3 == 2: S[p] = 0
            elif a and not b: S[q] = a            # reproduction
            elif b and not a: S[p] = b
    if render:
        fig, ax = plt.subplots(figsize=(6,6)); w = PillowWriter(fps=12); t0=time.time()
        with w.saving(fig, f"{out}.gif", dpi=80):
            for g in range(gens):
                gen()
                if g % 6 == 0:
                    ax.clear(); ax.imshow(S.reshape(side,side), cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
                    ax.set_title(f"spatial RPS + mobility (pe={pe})  gen={g}", fontsize=9)
                    ax.set_xticks([]); ax.set_yticks([]); w.grab_frame()
        ax.clear(); ax.imshow(S.reshape(side,side), cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
        ax.set_xticks([]); ax.set_yticks([]); fig.savefig(f"{out}_last.png", dpi=120, bbox_inches='tight'); plt.close()
        print(f"pe={pe} rendered {gens} gens in {round(time.time()-t0)}s")
    else:
        for g in range(gens): gen()
    return S

if __name__ == "__main__":
    run(side=128, gens=500, pe=0.10, seed=1, out="out/_spiral")
