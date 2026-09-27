"""Convert every Highlights post not yet annotated into annotated/skeletons/<slug>.tex
and run the verbatim check on each. Usage: python src/make_skeletons.py"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / ".venv" / "bin" / "python")
ALREADY_ANNOTATED = {"twelve-virtues-of-rationality", "the-bottom-line",
                     "making-beliefs-pay-rent-in-anticipated-experiences",
                     "humans-are-not-automatically-strategic"}

manifest = json.loads((ROOT / "data/manifests/highlights.json").read_text())
failures = 0
for e in manifest:
    if e["slug"] in ALREADY_ANNOTATED:
        continue
    out = ROOT / "annotated/skeletons" / f"{e['slug']}.tex"
    out.parent.mkdir(exist_ok=True)
    subprocess.run([PY, str(ROOT / "src/md2tex.py"), e["slug"], str(out), e["title"], e["author"],
                    e["posted_at"][:4], e["url"]], check=True, capture_output=True)
    r = subprocess.run([PY, str(ROOT / "src/check_verbatim.py"), str(out),
                        str(ROOT / "data/originals" / f"{e['slug']}.md")], capture_output=True, text=True)
    print(r.stdout.strip()[:1500])
    failures += r.returncode != 0
print("failures:", failures)
sys.exit(1 if failures else 0)
