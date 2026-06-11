"""Self-healing overnight driver for E5 + E6 collection.

Background jobs in this environment get killed before slow reasoning models finish. This
driver polls coverage, dedups duplicate appends (concurrent-writer safety), and relaunches
any run.py that has died, until both experiments reach their expected row counts. Single
writer per experiment is enforced by only relaunching when no run.py for that experiment is
alive. Prints a progress line each loop; exits when both complete or after a hard deadline.
"""
import json
import os
import subprocess
import time

BASE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(BASE, ".venv", "bin", "python")
KEY = ("model", "task_id", "trial", "condition")

EXPECTED = {
    "e5-latency-decoupled": 5 * 16 * 3 * 2,   # 480
    "e6-length-bias": 6 * 10 * 3 * 4,         # 720
}
DEADLINE = time.time() + 3 * 3600  # 3h hard stop


def dedup(path):
    if not os.path.exists(path):
        return 0
    rows = [json.loads(l) for l in open(path) if l.strip()]
    seen = {}
    for r in rows:
        seen[tuple(r.get(k) for k in KEY)] = r
    with open(path, "w") as f:
        for r in seen.values():
            f.write(json.dumps(r) + "\n")
    return len(seen)


def alive(exp):
    """A run.py for this experiment is alive iff some run.py process has its cwd in the
    experiment dir. Command lines are identical across experiments, so we must inspect
    /proc/<pid>/cwd rather than the cmdline."""
    expdir = os.path.join(BASE, exp)
    res = subprocess.run("pgrep -f 'run.py'", shell=True, capture_output=True, text=True)
    for pid in res.stdout.split():
        try:
            cwd = os.readlink(f"/proc/{pid}/cwd")
        except OSError:
            continue
        if os.path.realpath(cwd) == os.path.realpath(expdir):
            return True
    return False


def relaunch(exp):
    d = os.path.join(BASE, exp)
    subprocess.Popen(f"nohup {PY} run.py >> driver_run.log 2>&1 &",
                     shell=True, cwd=d)


def main():
    done = {e: False for e in EXPECTED}
    while time.time() < DEADLINE:
        line = []
        for exp, exp_total in EXPECTED.items():
            path = os.path.join(BASE, exp, "results.jsonl")
            n = dedup(path)
            running = alive(exp)
            if n >= exp_total:
                done[exp] = True
            elif not running:
                relaunch(exp)
            line.append(f"{exp.split('-')[0]}={n}/{exp_total}{'*' if running else ''}")
        print(time.strftime("%H:%M:%S"), " ".join(line), flush=True)
        if all(done.values()):
            print("ALL COMPLETE", flush=True)
            return
        time.sleep(30)
    print("DEADLINE REACHED", flush=True)


if __name__ == "__main__":
    main()
