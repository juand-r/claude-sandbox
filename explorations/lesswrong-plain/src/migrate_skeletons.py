"""Carry the annotated posts over to a new version of src/md2tex.py.

Usage:
    python src/migrate_skeletons.py OLD_MD2TEX [--apply] [--rebase] [slug ...]

For each post, the skeleton is made with the old converter (OLD_MD2TEX, a copy of the
previous src/md2tex.py placed in src/ so that its paths resolve) and with the current one.
Where they differ, the converter's changes are applied to the annotated post's text,
keeping our notes and any hand edits. A converter change that overlaps a hand edit is not
applied; the post is reported for a decision by hand.

With --rebase (for posts whose hand edits were markup repairs that the new converter now
makes itself), the post text is replaced by the new skeleton and the notes are moved to the
matching positions; any remaining hand edit is lost, so check the diff.

Without --apply, only reports what would change. Run check_verbatim and notes_backup
export afterwards.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_backup import POSTS, POST_HEADER, PY, ROOT, diff_ops, join_notes, split_notes, unescape_header  # noqa: E402


def skeleton(script: Path, post_text: str) -> str:
    title, author, year, url = POST_HEADER.match(post_text).groups()
    orig_slug = url.rstrip("/").split("/")[-1]
    with tempfile.NamedTemporaryFile("r", suffix=".tex") as tmp:
        subprocess.run([PY, str(script), orig_slug, tmp.name, unescape_header(title),
                        unescape_header(author), year, url], check=True, capture_output=True)
        return Path(tmp.name).read_text()


def map_pos(pos: int, hand: list) -> int | None:
    """Map a position in the old skeleton to the annotated text; None if inside a hand edit."""
    shift = 0
    for op in hand:
        if op["at"] + op["del_len"] <= pos and not (op["del_len"] == 0 and op["at"] == pos):
            shift += len(op["ins"]) - op["del_len"]
        elif op["at"] < pos < op["at"] + op["del_len"]:
            return None
    return pos + shift


def rebase(text: str, notes: list, s_new: str):
    """Move the notes from text onto s_new, following the character diff between them."""
    ops = diff_ops(text, s_new)
    moved = []
    for n, src in notes:
        shift = sum(len(op["ins"]) - op["del_len"] for op in ops if op["at"] + op["del_len"] <= n)
        moved.append((n + shift, src))
    return s_new, moved


def migrate(slug: str, old_script: Path, apply: bool, do_rebase: bool = False) -> str:
    post = (POSTS / f"{slug}.tex").read_text()
    s_old, s_new = skeleton(old_script, post), skeleton(ROOT / "src/md2tex.py", post)
    if s_old == s_new:
        return "same"
    text, notes = split_notes(post)
    if do_rebase:
        new_text, new_notes = rebase(text, notes, s_new)
        if apply:
            (POSTS / f"{slug}.tex").write_text(join_notes(new_text, new_notes))
        return f"rebased ({len(diff_ops(text, s_new))} text differences replaced by the new skeleton)"
    hand = diff_ops(s_old, text)
    conv = diff_ops(s_old, s_new)
    touched = [(op["at"], op["at"] + op["del_len"]) for op in hand]
    mapped = []
    for op in conv:
        a, b = op["at"], op["at"] + op["del_len"]
        if any(x < b and a < y or (a == b and x <= a <= y and y > x) for x, y in touched):
            return f"CONFLICT at old-skeleton offset {a}: {s_old[max(0, a - 40):b + 40]!r}"
        t_at = map_pos(a, hand)
        if t_at is None:
            return f"CONFLICT (inside hand edit) at {a}"
        mapped.append((t_at, op["del_len"], op["ins"]))
    new_text, new_notes = text, list(notes)
    for t_at, dl, ins in sorted(mapped, reverse=True):
        new_text = new_text[:t_at] + ins + new_text[t_at + dl:]
        delta = len(ins) - dl
        new_notes = [(n + delta if n > t_at else n, src) for n, src in new_notes]
    if apply:
        (POSTS / f"{slug}.tex").write_text(join_notes(new_text, new_notes))
    return f"changed ({len(conv)} converter edits, {len(hand)} hand edits kept)"


def main(argv):
    if not argv:
        sys.exit(__doc__)
    old_script = Path(argv[0]).resolve()
    apply, do_rebase = "--apply" in argv, "--rebase" in argv
    slugs = [a for a in argv[1:] if not a.startswith("--")] or sorted(p.stem for p in POSTS.glob("*.tex"))
    for s in slugs:
        r = migrate(s, old_script, apply, do_rebase)
        if r != "same":
            print(f"{s}: {r}")


if __name__ == "__main__":
    main(sys.argv[1:])
