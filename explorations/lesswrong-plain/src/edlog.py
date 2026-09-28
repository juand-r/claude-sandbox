"""Exact, logged replacements in one file (the editor's final pass, docs/STANDARDS.md section 8).

Use from Python:
    import sys; sys.path.insert(0, "src")
    from edlog import apply
    apply("honest/sections/<slug>.tex", [(old, new), ...], log="docs/raz/changes/<batch>.md",
          why="one line: the rule or finding behind these edits")

Each `old` must occur exactly once, or nothing is written. Every edit is appended to the
log as Before/After. For posts, run src/check_verbatim.py afterwards.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def apply(rel_path: str, edits: list, log: str, why: str = "") -> None:
    path = ROOT / rel_path
    text = path.read_text()
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{rel_path}: expected 1 match, found {n}: {old[:90]!r}")
        text = text.replace(old, new)
    path.write_text(text)
    log_path = ROOT / log
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as f:
        f.write(f"\n## {rel_path}\n\n")
        if why:
            f.write(f"Why: {why}\n\n")
        for old, new in edits:
            f.write(f"- Before: {old}\n- After: {new}\n\n")
    print(f"{rel_path}: {len(edits)} edits")
