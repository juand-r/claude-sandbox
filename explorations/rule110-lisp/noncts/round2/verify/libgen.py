"""Build my independent compound library (E^2..E^9, GB1..GB8, tight A^k
later) from Martinez gliders by my own collisions; cache to lib_v1.pkl."""
import pickle, os, vlib

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib_v1.pkl")


def generate():
    vlib.init_martinez()
    prev = "E"
    for n in range(2, 10):
        row, org, _ = vlib.build([(prev, 0, 0), ("B", 0, 80)], T=400)
        vlib.harvest(f"E^{n}", vlib.evolve(row, 400), 400, which="all")
        prev = f"E^{n}"
    prev = "G"
    for k in range(1, 9):
        row, org, _ = vlib.build([(prev, 0, 0), ("B", 0, 90)], T=600)
        vlib.harvest(f"GB{k}", vlib.evolve(row, 600), 600, which="all")
        prev = f"GB{k}"
    # tight A packets, harvested from counter answers (my own runs, t5.py):
    # E^2 + GB1 -> E + A^2, E^2 + G -> E + A^3 (every class), E + G -> E + A^4
    T = 800
    for nm, scene in (("A^2", [("E^2", 0, 0), ("GB1", 0, 30)]),
                      ("A^3", [("E^2", 0, 0), ("G", 0, 30)])):
        row, org, _ = vlib.build(scene, T=T)
        vlib.harvest(nm, vlib.evolve(row, T), T, which=0)
    for t0 in range(42):
        row, org, _ = vlib.build([("E", 0, 0), ("G", t0, 30)], T=T)
        r = vlib.evolve(row, T)
        ids = vlib.identify(r, T=T)
        if [i[0].split("@")[0] for i in ids] == ["E", "?"] and ids[1][2] == 4:
            vlib.harvest("A^4", r, T, which=0)
            break
    order = list(vlib.LIB)
    pickle.dump([(n, vlib.LIB[n].base, (vlib.LIB[n].P, vlib.LIB[n].D)) for n in order],
                open(CACHE, "wb"))


def load():
    if not os.path.exists(CACHE):
        generate()
        return
    vlib.LIB.clear(); vlib.KEYS.clear(); vlib.MULTI.clear()
    for n, base, per in pickle.load(open(CACHE, "rb")):
        vlib.register(n, base, per)


if __name__ == "__main__":
    generate()
    print({n: (g.P, g.D, g.w) for n, g in vlib.LIB.items()})
