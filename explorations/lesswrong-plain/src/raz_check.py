"""Mechanical checks for one post in both editions (docs/STANDARDS.md, section 7).

Usage: python src/raz_check.py <slug> [<slug> ...]

For each slug it reports:
  - verbatim check of annotated/posts/<slug>.tex against data/originals/<slug>.md
  - paragraph and \\cpara counts, Summary/Response words, "In short:" (via src/audit.py)
  - every ``quotation'' in our text (notes, afterword, honest section) that does not occur
    in the post: each must be either fixed or accounted for in the agent's report
  - flags to read by hand: reserved words (STANDARDS 2.3), third-person pronouns,
    motive-reading phrases, em dashes, italics, banned phrases
It never edits anything. Exit status 1 if the verbatim check fails or a file is missing.
"""

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / ".venv/bin/python")
OUR_NOTES = ("cpara", "clogic", "cfact", "cstyle", "ccut")  # \cauthor is the post's footnote

RESERVED = r"\b(false|falsely|wrong|refutes?|refuted|contradicts?|contradiction|the opposite|backwards|never|cannot fail|unfalsifiable|invented|invents|misquot\w*|rigged)\b"
PRONOUNS = r"\b(he|his|him|himself|she|her|hers|herself)\b"
MOTIVE = r"\b(my reading|i infer|inference|flatter\w*|invites the reader|feel superior|exists to|is for everyone else)\b"
BANNED = ["load-bearing", "it is worth noting", "here's the thing", "smoking gun", "real gap",
          "notably", "importantly", "crucially", "delve", "underscores", "doing a lot of work",
          "belt-and-suspenders", "genuine gap", "honestly"]


def braced(text: str, start: int) -> tuple[str, int]:
    """Return (content, end index) of the brace group opening at text[start] == '{'."""
    depth, j = 1, start + 1
    while depth:
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        j += 1
    return text[start + 1:j - 1], j


def macro_bodies(text: str, names) -> list[str]:
    out = []
    for m in re.finditer(r"\\(%s)\{" % "|".join(names), text):
        out.append(braced(text, m.end() - 1)[0])
    return out


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("—", "---"), ("–", "--"),
                 ("…", "..."), ("\u00a0", " "), ("`", "'"), ('"', "'")]:
        s = s.replace(a, b)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # markdown links
    s = re.sub(r"\\(emph|textbf|textit|textsc)\{", "", s)
    s = s.replace("*", "").replace("\\", "").replace("{", "").replace("}", "").replace("~", " ")
    return re.sub(r"\s+", " ", s).lower()


def known_titles() -> set:
    """Titles of every fetched original (their first line), normalized."""
    out = set()
    for f in (ROOT / "data/originals").glob("*.md"):
        first = f.read_text().split("\n", 1)[0]
        out.add(norm(first.lstrip("# ")).strip(" ,.;:"))
    return out


TITLES = None


def quotes_not_in_post(ours: str, original: str) -> list[str]:
    global TITLES
    TITLES = TITLES if TITLES is not None else known_titles()
    orig = norm(original)
    missing = []
    for q in re.findall(r"``(.*?)''", ours, re.S):
        pieces = [p.strip(" ,.;:") for p in re.split(r"\\ldots|\.\.\.|\[[^\]]*\]", q)]
        pieces = [norm(p).strip(" ,.;:") for p in pieces if p.strip(" ,.;:")]
        if norm(q).strip(" ,.;:?") in TITLES or norm(q).strip(" ,.;:") in TITLES:
            continue
        if any(p not in orig and p.replace("---", "--") not in orig for p in pieces):
            missing.append(q.replace("\n", " ")[:110])
    return missing


def flags(label: str, text: str) -> list[str]:
    out = []
    for m in re.finditer(RESERVED, text, re.I):
        out.append(f"reserved '{m.group(0)}': ...{text[max(0, m.start()-60):m.end()+40]}...")
    for m in re.finditer(PRONOUNS, text, re.I):
        out.append(f"pronoun '{m.group(0)}': ...{text[max(0, m.start()-60):m.end()+30]}...")
    for m in re.finditer(MOTIVE, text, re.I):
        out.append(f"motive? '{m.group(0)}': ...{text[max(0, m.start()-60):m.end()+40]}...")
    if "—" in text or "---" in text:
        out.append("em dash in our text")
    if re.search(r"\\(emph|textit)\{", text):
        out.append("italics in our text")
    for b in BANNED:
        if b in text.lower():
            out.append(f"banned phrase '{b}'")
    return [f"  [{label}] {f}".replace("\n", " ") for f in out]


def check(slug: str) -> bool:
    ok = True
    post_f = ROOT / "annotated/posts" / f"{slug}.tex"
    aft_f = ROOT / "annotated/afterwords" / f"{slug}.tex"
    hon_f = ROOT / "honest/sections" / f"{slug}.tex"
    orig_f = ROOT / "data/originals" / f"{slug}.md"
    print(f"== {slug}")
    for f in (post_f, aft_f, hon_f, orig_f):
        if not f.exists():
            print(f"  MISSING {f.relative_to(ROOT)}")
            ok = False
    if not ok:
        return False
    r = subprocess.run([PY, str(ROOT / "src/audit.py"), slug], capture_output=True, text=True)
    print("\n".join("  " + line.strip() for line in r.stdout.splitlines()
                    if not line.strip().startswith("praise-word") and not line.startswith("==")))
    if "verbatim: OK" not in r.stdout:
        ok = False
    post, aft, hon = post_f.read_text(), aft_f.read_text(), hon_f.read_text()
    original = orig_f.read_text()
    notes = "\n".join(macro_bodies(post, OUR_NOTES))
    nbs = "\n".join(macro_bodies(hon, ("nb",)))
    for label, text in [("notes", notes), ("afterword", aft), ("honest", hon)]:
        miss = quotes_not_in_post(text, original)
        for q in miss:
            print(f"  [{label}] quote not in post (fix, or source it in the report): {q}")
    hon_words = len(re.sub(r"\\[a-z]+", " ", hon).split())
    print(f"  honest words: {hon_words}, n.b. notes: {len(macro_bodies(hon, ('nb',)))}")
    for label, text in [("notes", notes), ("afterword", aft), ("honest n.b.", nbs)]:
        for line in flags(label, text):
            print(line[:220])
    return ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    results = [check(s) for s in sys.argv[1:]]
    sys.exit(0 if all(results) else 1)
