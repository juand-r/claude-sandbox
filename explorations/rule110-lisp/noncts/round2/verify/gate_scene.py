"""Get gate's scene (their placement rule) for a program, as plain data.
Imports gate/stream.py read-only (it chdirs into collider/)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.abspath(os.path.join(HERE, "..", "gate"))
sys.path.insert(0, GATE)
cwd = os.getcwd()
import stream          # noqa: E402
os.chdir(cwd)

def scene(program, **kw):
    sc = stream.build(program, **kw)
    return [(g, int(t), int(x)) for g, t, x in sc]

if __name__ == "__main__":
    print(json.dumps(scene(list(sys.argv[1]))))
