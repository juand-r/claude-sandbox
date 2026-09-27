"""Audit annotated posts against the README's mechanical requirements.

For each posts/<name>.tex that has an afterword: verbatim check, paragraph count vs
\\cpara count, note counts, praise words to read by hand, Summary/Response lengths, and
the "In short:" line. Usage: python src/audit.py [name ...]
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_verbatim import take_braced  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ANN = ROOT / "annotated"
PY = str(ROOT / ".venv/bin/python")
SLUG_FOR_FILE = {"making-beliefs-pay-rent": "making-beliefs-pay-rent-in-anticipated-experiences",
                 "pr-is-corrosive": "pr-is-corrosive-reputation-is-not"}
PRAISE = r"\b(best|good|great|well|fair|strong|clear|sharp|excellent|elegant|memorable|useful|sound|insightful|effective|compelling|admirabl\w*|valuable|nice)\b"


def notes(tex):
    out = []
    for m in re.finditer(r"\\c(para|style|logic|fact|cut)\{", tex):
        arg, _ = take_braced(tex, m.end() - 1)
        out.append((m.group(1), arg))
    return out


def words(tex):
    tex = re.sub(r"\\[a-z]+\*?(\{[^}]*\})?", " ", tex)
    return len(re.findall(r"[A-Za-z0-9'’]+", tex))


def audit(name):
    post = (ANN / "posts" / f"{name}.tex").read_text()
    aw = (ANN / "afterwords" / f"{name}.tex").read_text()
    slug = SLUG_FOR_FILE.get(name, name)
    r = subprocess.run([PY, str(ROOT / "src/check_verbatim.py"), str(ANN / "posts" / f"{name}.tex"),
                        str(ROOT / "data/originals" / f"{slug}.md")], capture_output=True, text=True)
    paras = sum(1 for ln in post.split("\n") if ln.rstrip().endswith(r"\flushnotes") and not ln.lstrip().startswith(r"\end{"))
    ns = notes(post)
    kinds = {k: sum(1 for kk, _ in ns if kk == k) for k in ["para", "style", "logic", "fact", "cut"]}
    praise = [(k, m.group(0), t[:90]) for k, t in ns for m in [re.search(PRAISE, t, re.I)] if m]
    summary, _, response = aw.partition(r"\responsehead")
    in_short = re.search(r"In short:", response) is not None
    print(f"== {name}")
    print(f"   verbatim: {r.stdout.split()[0] if r.stdout else 'ERROR'}   paragraphs: {paras}   notes: {len(ns)} {kinds}")
    print(f"   summary words: {words(summary)}   response words: {words(response)}   'In short:': {in_short}")
    for k, w, t in praise:
        print(f"   praise-word? [{k}] '{w}': {t}")


def main(names):
    if not names:
        names = sorted(p.stem for p in (ANN / "afterwords").glob("*.tex"))
    for n in names:
        audit(n)


if __name__ == "__main__":
    main(sys.argv[1:])
