"""Check that the main text of each annotated post matches the original word for word.

Usage:
    python src/check_verbatim.py annotated/posts/the-bottom-line.tex data/originals/the-bottom-line.md

Strips my commentary notes and LaTeX markup from the .tex file, strips Markdown markup
from the original, normalizes quotes and whitespace, and diffs the two word sequences.
The author's own footnotes (\\cauthor{...}) are compared too: they are moved to the end
of the text, which is where the original Markdown puts them.
Exits with status 1 and prints the differences if the texts differ.
"""

import difflib
import unicodedata
import re
import sys
from pathlib import Path

COMMENT_MACROS = ["cpara", "cstyle", "clogic", "cfact", "ccut", "cgood"]
AUTHOR_MACRO = "cauthor"


def take_braced(s: str, start: int) -> tuple[str, int]:
    """s[start] must be '{'. Return (contents, index after the matching '}')."""
    assert s[start] == "{", s[start:start + 30]
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{" and s[i - 1] != "\\":
            depth += 1
        elif s[i] == "}" and s[i - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
    raise ValueError("unbalanced braces")


def remove_macro(s: str, name: str) -> tuple[str, list[str]]:
    """Remove every \\name{...}; return the new text and the removed arguments."""
    removed, out, i = [], [], 0
    pat = re.compile(r"\\" + name + r"\{")
    while (m := pat.search(s, i)):
        out.append(s[i:m.start()])
        arg, i = take_braced(s, m.end() - 1)
        removed.append(arg)
    out.append(s[i:])
    return "".join(out), removed


def unwrap(s: str, name: str, keep_arg: int, nargs: int) -> str:
    """Replace \\name{a1}...{an} by its keep_arg-th argument (1-based)."""
    pat = re.compile(r"\\" + name + r"\{")
    while (m := pat.search(s)):
        args, j = [], m.end() - 1
        for _ in range(nargs):
            arg, j = take_braced(s, j)
            args.append(arg)
        s = s[:m.start()] + args[keep_arg - 1] + s[j:]
    return s


def tex_to_text(tex: str) -> str:
    tex = re.sub(r"^\\post\{.*$", "", tex, flags=re.M)
    for name in COMMENT_MACROS:
        tex, _ = remove_macro(tex, name)
    tex, author_notes = remove_macro(tex, AUTHOR_MACRO)
    tex = tex + "\n" + "\n".join(author_notes)
    tex, _ = remove_macro(tex, "figph")  # image placeholders (images are dropped on both sides)
    tex, _ = remove_macro(tex, "fnnum")  # footnote numbers (dropped on both sides)
    tex = unwrap(tex, "href", keep_arg=2, nargs=2)
    for name in ["emph", "textbf", "url", "posthead"]:
        tex = unwrap(tex, name, keep_arg=1, nargs=1)
    tex = re.sub(r"\\(flushnotes|item|quad)\b", " ", tex)
    tex = re.sub(r"\\(begin|end)\{\w+\}", " ", tex)
    tex = tex.replace("\\\\", " ")  # table row ends
    for esc, ch in [(r"\textbackslash{}", "\\"), (r"\^{}", "^"), (r"\~{}", "~"), (r"\{", "{"), (r"\}", "}"),
                    (r"\$", "$"), (r"\&", "&"), (r"\#", "#"), (r"\_", "_"), (r"\%", "%")]:
        tex = tex.replace(esc, ch)
    tex = tex.replace("-{}-", "--")
    tex = tex.replace("``", "\"").replace("''", "\"")
    return tex


def md_to_text(md: str, move_notes: bool = True) -> str:
    md = md.split("\n---\n", 1)[1]  # drop the header written by fetch.py
    md = re.sub(r"\[(\d+)\]\(#[^)]*\)", "", md)  # footnote markers like [1](#fn1x27)
    md = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", md)  # linked images
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)  # images
    md = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]*)(?:\s+\"[^\"]*\")?\)", r"\1", md)  # links -> text
    md = re.sub(r"^```.*$", "", md, flags=re.M)  # code fences
    md = re.sub(r"^\|[\s|:-]+\|$", "", md, flags=re.M)  # table separator rows
    md = re.sub(r"^\|(.*)\|$", lambda m: m.group(1).replace("|", " "), md, flags=re.M)  # table rows
    md = re.sub(r"<(http[^>]*)>", r"\1", md)  # autolinks
    md = re.sub(r"(?<!\\)\[\d+\](?!\()", "", md)  # bare, unescaped footnote markers like [1]
    md = re.sub(r"\\([\\`_{}\[\]()#+\-.!|>])", r"\1", md)  # other Markdown escapes (\[1\] is literal text)
    md = md.replace(r"\*", "\x00")  # escaped literal asterisks survive
    md = md.replace("**", "").replace("*", "").replace("\x00", "*")
    md = re.sub(r"^\s*> ?", "", md, flags=re.M)  # blockquote markers
    md = re.sub(r"^\s*[*-] ", "", md, flags=re.M)  # bullet markers
    md = re.sub(r"^\s*\d+\. ", "", md, flags=re.M)  # numbered-list markers
    # Footnote list written as "###### 1. text" headings: move it to the end, where
    # the annotated file's author footnotes end up, and drop the numbering.
    # (Only when the annotated file moved them into \cauthor notes; when it keeps them in
    # place as \fnnum paragraphs, leave them where they are.)
    notes = re.findall(r"^#+ \d+\. (.*)$", md, flags=re.M) if move_notes else []
    if move_notes:
        md = re.sub(r"^#+ \d+\. .*$", "", md, flags=re.M)
    else:
        md = re.sub(r"^#+ \d+\. ", "", md, flags=re.M)  # kept in place; numbers are \fnnum
    md = re.sub(r"^---+$", "", md, flags=re.M)  # horizontal rules
    md = re.sub(r"^#{1,6}\s*", "", md, flags=re.M)  # heading markers
    return md + "\n" + "\n".join(notes)


def normalize(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text)  # e.g. "é" as one or two code points
    for a, b in [("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'")]:
        text = text.replace(a, b)
    return text.split()


def main(tex_path: str, md_path: str) -> int:
    tex_src = Path(tex_path).read_text()
    got = normalize(tex_to_text(tex_src))
    want = normalize(md_to_text(Path(md_path).read_text(), move_notes="\\fnnum{" not in tex_src))
    if got == want:
        print(f"OK  {tex_path}: {len(got)} words match")
        return 0
    print(f"DIFF {tex_path}")
    sm = difflib.SequenceMatcher(a=want, b=got, autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != "equal":
            print(f"  {op}: original={' '.join(want[a1:a2])!r}  annotated={' '.join(got[b1:b2])!r}")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
