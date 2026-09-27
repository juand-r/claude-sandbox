"""Extract our own prose (notes and afterwords) per post, for review and style scans.
Usage: python src/prose.py scan            -> style-rule hits across all posts
       python src/prose.py show <name>     -> the post's paragraphs (first words) with their notes, then the afterword
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_verbatim import take_braced
ANN = Path(__file__).resolve().parent.parent / "annotated"
KINDS = "para|style|logic|fact|cut"

def notes(tex):
    out = []
    for m in re.finditer(r"\\c(" + KINDS + r")\{", tex):
        a, _ = take_braced(tex, m.end() - 1)
        out.append((m.start(), m.group(1), a))
    return out

def our_text(name):
    post = (ANN / "posts" / f"{name}.tex").read_text()
    aw = (ANN / "afterwords" / f"{name}.tex").read_text()
    return [(k, t) for _, k, t in notes(post)] + [("afterword", aw)]

RULES = {
    "italics": r"\\emph\{", "em dash": r"—|---", "intensifier": r"\b(clearly|obviously|notably|importantly|undoubtedly|crucially|simply put)\b",
    "signpost": r"\b(The key point|The central finding|It is worth noting|The headline|Here's the thing|load-bearing)\b",
    "not X but Y": r"\bis not \w+[^.;]{0,40}, it is\b|\bnot just\b",
}

def scan():
    names = sorted(p.stem for p in (ANN / "afterwords").glob("*.tex"))
    tot = {k: 0 for k in RULES}
    for n in names:
        for kind, t in our_text(n):
            # quoted material from the post is allowed its own style: drop ``...''
            t2 = re.sub(r"``.*?''", "", t, flags=re.S)
            for r, pat in RULES.items():
                for m in re.finditer(pat, t2):
                    tot[r] += 1
                    print(f"{n} [{kind}] {r}: ...{t2[max(0,m.start()-60):m.end()+60]!r}")
    print(tot)

def show(name):
    post = (ANN / "posts" / f"{name}.tex").read_text()
    for line in post.split("\n"):
        if not line.strip(): continue
        ns = notes(line)
        body = re.sub(r"\\c(" + KINDS + r"|author)\{", "\x00", line)
        text = line
        for _, k, t in ns:
            text = text.replace("\\c" + k + "{" + t + "}", "")
        text = re.sub(r"\\(flushnotes|emph|textbf|href\{[^}]*\})", "", text)
        print("TEXT:", " ".join(text.split()))
        for _, k, t in ns:
            print(f"   [{k}] {t}")
    print("\n===== AFTERWORD =====\n" + (ANN / "afterwords" / f"{name}.tex").read_text())

if __name__ == "__main__":
    {"scan": lambda: scan(), "show": lambda: show(sys.argv[2])}[sys.argv[1]]()
