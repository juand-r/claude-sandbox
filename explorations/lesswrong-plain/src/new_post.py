"""Create annotated/posts/<slug>.tex from the verbatim skeleton, for a post in the
Rationality: A-Z manifest, and run the verbatim check. Refuses to overwrite.

Usage: python src/new_post.py <slug>
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / ".venv/bin/python")

slug = sys.argv[1] if len(sys.argv) == 2 else sys.exit(__doc__)
entry = {e["slug"]: e for e in json.loads((ROOT / "data/manifests/rationality_az.json").read_text())}.get(slug)
if entry is None:
    sys.exit(f"{slug} is not in data/manifests/rationality_az.json")
out = ROOT / "annotated/posts" / f"{slug}.tex"
if out.exists():
    sys.exit(f"{out.relative_to(ROOT)} already exists; not overwriting")
subprocess.run([PY, str(ROOT / "src/md2tex.py"), slug, str(out), entry["title"], entry["author"],
                entry["posted_at"][:4], entry["url"]], check=True, capture_output=True)
r = subprocess.run([PY, str(ROOT / "src/check_verbatim.py"), str(out),
                    str(ROOT / "data/originals" / f"{slug}.md")], capture_output=True, text=True)
print(r.stdout.strip()[:500])
sys.exit(r.returncode)
