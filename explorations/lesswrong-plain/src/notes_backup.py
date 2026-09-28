"""Back up the commentary in annotated/posts/*.tex without the post text, and restore it.

The post files hold each LessWrong post verbatim, so they are not committed (the repo is
public and the authors keep copyright). This script stores only what we added: the
difference between the verbatim skeleton (made by src/md2tex.py from data/originals/) and
the annotated file. The stored patch holds our notes and the character offsets where they
go. Deleted skeleton text is never stored, only its length and hash.

Usage:
    python src/notes_backup.py export [slug ...]   # annotated/posts -> annotated/notes/*.json
    python src/notes_backup.py restore [slug ...]  # annotated/notes + originals -> annotated/posts
    python src/notes_backup.py check               # export would change nothing; restore is exact

Restore needs data/originals/<slug>.md (python src/fetch.py post <id>). If the original
has changed on LessWrong since export, the skeleton hash will differ and restore stops.
"""

import difflib
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "annotated" / "posts"
NOTES = ROOT / "annotated" / "notes"
PY = sys.executable
POST_HEADER = re.compile(r"^\\post\{(.*?)\}\{(.*?)\}\{(\d{4})\}\{(\S+?)\}\n")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def unescape_header(s: str) -> str:
    """Inverse of md2tex.escape_tex for the characters that occur in titles."""
    for esc, ch in [(r"\textbackslash{}", "\\"), (r"\{", "{"), (r"\}", "}"), (r"\$", "$"),
                    (r"\&", "&"), (r"\#", "#"), (r"\%", "%"), (r"\_", "_"), ("-{}-", "--")]:
        s = s.replace(esc, ch)
    return s


def skeleton_for(post_text: str) -> str:
    """Regenerate the verbatim skeleton from the post's own \\post header."""
    m = POST_HEADER.match(post_text)
    if not m:
        raise SystemExit("post file does not start with a \\post{...} header")
    title, author, year, url = m.groups()
    orig_slug = url.rstrip("/").split("/")[-1]
    with tempfile.NamedTemporaryFile("r", suffix=".tex") as tmp:
        subprocess.run([PY, str(ROOT / "src/md2tex.py"), orig_slug, tmp.name,
                        unescape_header(title), unescape_header(author), year, url],
                       check=True, capture_output=True)
        return Path(tmp.name).read_text()


def diff_ops(a: str, b: str) -> list:
    """Character-level edit ops from a to b. Lines are matched first, so this is fast;
    only changed runs of lines are compared character by character."""
    al, bl = a.splitlines(keepends=True), b.splitlines(keepends=True)
    aoff, boff = [0], [0]
    for line in al:
        aoff.append(aoff[-1] + len(line))
    for line in bl:
        boff.append(boff[-1] + len(line))
    ops = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, al, bl, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        sa, sb = a[aoff[i1]:aoff[i2]], b[boff[j1]:boff[j2]]
        for t, k1, k2, m1, m2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
            if t != "equal":
                at = aoff[i1] + k1
                ops.append({"at": at, "del_len": k2 - k1, "del_sha": sha(a[at:at + k2 - k1]),
                            "ins": sb[m1:m2]})
    return ops


NOTE_MACROS = ("cpara", "clogic", "cfact", "cstyle", "ccut")  # \cauthor is the post's own footnote
NOTE_START = re.compile(r"\\(%s)\{" % "|".join(NOTE_MACROS))


def split_notes(post: str):
    """Return (text without our notes, [(index in that text, note source)])."""
    text, notes, i = [], [], 0
    n = 0  # length of text so far
    while True:
        m = NOTE_START.search(post, i)
        if not m:
            text.append(post[i:])
            break
        text.append(post[i:m.start()])
        n += m.start() - i
        j, depth = m.end(), 1
        while depth:
            depth += {"{": 1, "}": -1}.get(post[j], 0)
            j += 1
        notes.append((n, post[m.start():j]))
        i = j
    return "".join(text), notes


def join_notes(text: str, notes: list) -> str:
    out, pos = [], 0
    for at, src in notes:
        out.append(text[pos:at])
        out.append(src)
        pos = at
    out.append(text[pos:])
    return "".join(out)


def export(slug: str) -> dict:
    post = (POSTS / f"{slug}.tex").read_text()
    skel = skeleton_for(post)
    text, notes = split_notes(post)
    edits = diff_ops(skel, text)
    data = {"slug": slug, "header": POST_HEADER.match(post).group(0), "skeleton_sha": sha(skel),
            "post_sha": sha(post), "edits": edits, "notes": notes}
    NOTES.mkdir(exist_ok=True)
    (NOTES / f"{slug}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return data


def rebuild(data: dict, skel: str) -> str:
    if sha(skel) != data["skeleton_sha"]:
        raise SystemExit(f"{data['slug']}: skeleton differs from the one exported "
                         "(original changed?); restore by hand")
    out, pos = [], 0
    for op in data["edits"]:
        out.append(skel[pos:op["at"]])
        if sha(skel[op["at"]:op["at"] + op["del_len"]]) != op["del_sha"]:
            raise SystemExit(f"{data['slug']}: deleted text mismatch at {op['at']}")
        out.append(op["ins"])
        pos = op["at"] + op["del_len"]
    out.append(skel[pos:])
    post = join_notes("".join(out), data["notes"])
    if sha(post) != data["post_sha"]:
        raise SystemExit(f"{data['slug']}: rebuilt file hash differs")
    return post


def restore(slug: str) -> None:
    data = json.loads((NOTES / f"{slug}.json").read_text())
    skel = skeleton_for(data["header"])  # the header line carries title, author, year, url
    (POSTS / f"{slug}.tex").write_text(rebuild(data, skel))


def main(argv):
    cmd, slugs = (argv[0], argv[1:]) if argv else ("", [])
    slugs = slugs or sorted(p.stem for p in (POSTS if cmd != "restore" else NOTES).glob("*.*"))
    if cmd == "export":
        for s in slugs:
            d = export(s)
            ins = sum(len(o["ins"]) for o in d["edits"])
            dl = sum(o["del_len"] for o in d["edits"])
            print(f"{s}: {len(d['notes'])} notes; text edits: {dl} chars deleted, {ins} inserted")
    elif cmd == "restore":
        for s in slugs:
            restore(s)
            print(f"restored {s}")
    elif cmd == "check":
        bad = 0
        for s in slugs:
            post = (POSTS / f"{s}.tex").read_text()
            data = json.loads((NOTES / f"{s}.json").read_text())
            try:
                ok = rebuild(data, skeleton_for(post)) == post
            except SystemExit as e:
                print(e); ok = False
            if not ok:
                bad += 1
                print(f"{s}: backup is stale or broken")
        print(f"{len(slugs) - bad}/{len(slugs)} backups exact")
        sys.exit(1 if bad else 0)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
