"""Convert a fetched post (data/originals/<slug>.md) into a verbatim LaTeX skeleton.

Usage:
    python src/md2tex.py <slug> <out.tex> "<post title>" "<author>" <year> <url>

The output is the post text for the left column of the annotated edition:
every paragraph line ends with \\flushnotes, the author's footnotes become \\cauthor{...}
at their markers, images become \\figph{...} placeholders, and LaTeX special characters
are escaped. No commentary is added. Always run src/check_verbatim.py on the result.
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGINALS = ROOT / "data" / "originals"

TEX_ESCAPES = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$", "&": r"\&",
    "#": r"\#", "%": r"\%", "_": r"\_", "^": r"\^{}", "~": r"\~{}",
}
PH = "\x00{}\x00"  # placeholder for protected LaTeX snippets


def escape_tex(text: str) -> str:
    out = "".join(TEX_ESCAPES.get(c, c) for c in text)
    return out.replace("--", "-{}-")  # keep double hyphens literal


def escape_url(url: str) -> str:
    return url.replace("\\", "/").replace("%", r"\%").replace("#", r"\#").replace("{", "").replace("}", "")


class Inline:
    """Converts one block of Markdown inline text to LaTeX."""

    def __init__(self):
        self.store = []

    def protect(self, tex: str) -> str:
        self.store.append(tex)
        return PH.format(len(self.store) - 1)

    def restore(self, text: str) -> str:
        while "\x00" in text:
            text = re.sub(r"\x00(\d+)\x00", lambda m: self.store[int(m.group(1))], text)
        return text

    def convert(self, md: str) -> str:
        # Markdown escapes such as \* \_ \[ become literal characters.
        # Plain footnote markers like [1] (not links) become small superscript numbers.
        md = re.sub(r"(?<!\\)\[(\d+)\](?!\()", lambda m: self.protect(r"\fnnum{" + m.group(1) + "}"), md)
        md = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>])", lambda m: self.protect(escape_tex(m.group(1))), md)
        # Linked images [![alt](src "t")](href) and images ![alt](src).
        md = re.sub(r"\[!\[([^\]]*)\]\(([^)\s]*)[^)]*\)\]\(([^)]*)\)",
                    lambda m: self.protect(r"\figph{" + escape_url(m.group(3)) + "}"), md)
        md = re.sub(r"!\[([^\]]*)\]\(([^)\s]*)[^)]*\)",
                    lambda m: self.protect(r"\figph{" + escape_url(m.group(2)) + "}"), md)
        # Autolinks <http://...>.
        md = re.sub(r"<(https?://[^>]+)>", lambda m: self.protect(r"\url{" + escape_url(m.group(1)) + "}"), md)
        # Links [text](url); the text is converted recursively.
        md = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]*)(?:\s+\"[^\"]*\")?\)",
                    lambda m: self.protect(r"\href{" + escape_url(m.group(2)) + "}{" + Inline().convert(m.group(1)) + "}"), md)
        md = escape_tex(md)
        # Emphasis, strongest first. Asterisks only; underscores were escaped above.
        md = re.sub(r"\*\*\*(.+?)\*\*\*", r"\\textbf{\\emph{\1}}", md, flags=re.S)
        md = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", md, flags=re.S)
        # Escaped literal asterisks were protected above, so every remaining single
        # asterisk is an emphasis marker, including intraword ones ("*actually*calculate").
        md = re.sub(r"(?<!\*)\*(?![\s*])(.+?)(?<![\s*])\*(?!\*)", r"\\emph{\1}", md, flags=re.S)
        return self.restore(md)


def inline(md: str) -> str:
    return Inline().convert(md)


def split_footnotes(body: str):
    """Pull out '[n](#fnNxK-bk)text' definitions and replace in-text markers with \\cauthor."""
    defs = {}
    kept = []
    for line in body.split("\n"):
        m = re.match(r"^\[(\d+)\]\(#(fn[^)]*)-bk\)\s*(.*)$", line)
        if m:
            defs[m.group(2)] = m.group(3)
        else:
            kept.append(line)
    body = "\n".join(kept)
    used = set()

    def marker(m):
        key = m.group(2)
        if key in defs:
            used.add(key)
            return "\x01AUTHORNOTE:" + key + "\x01"
        return ""
    body = re.sub(r"\[(\d+)\]\(#(fn[^)]*?)\)", marker, body)
    # Definitions without an in-text marker stay as plain paragraphs at the end.
    orphans = [t for k, t in defs.items() if k not in used]
    return body, defs, orphans


def convert_block(block: str, defs: dict) -> str:
    """Convert one Markdown block (separated by blank lines) to LaTeX."""
    lines = block.split("\n")
    first = lines[0]

    def with_notes(tex: str) -> str:
        return re.sub(r"\x01AUTHORNOTE:([^\x01]+)\x01",
                      lambda m: r"\cauthor{" + inline(defs[m.group(1)]) + "}", tex)

    if re.match(r"^```", first):
        inner = [l for l in lines if not l.startswith("```")]
        return with_notes(inline(" ".join(inner))) + r" \flushnotes"
    if re.match(r"^#{1,5} ", first):
        return r"\posthead{" + with_notes(inline(re.sub(r"^#+\s*", "", " ".join(lines)))) + r"} \flushnotes"
    if re.match(r"^###### ?\d+\.", first):
        num, text = re.match(r"^###### ?(\d+)\.\s*(.*)$", " ".join(lines)).groups()
        return r"\fnnum{" + num + "}" + with_notes(inline(text)) + r" \flushnotes"
    if re.match(r"^######\s*$", first) or re.match(r"^---+$", first):
        return ""  # empty heading or horizontal rule: layout only
    if first.startswith(">"):
        paras, cur = [], []
        for l in lines:
            l = re.sub(r"^>\s?", "", l)
            if l.strip():
                cur.append(l)
            elif cur:
                paras.append(" ".join(cur)); cur = []
        if cur:
            paras.append(" ".join(cur))
        body = "\n\n".join(with_notes(inline(p)) for p in paras)
        return "\\begin{quote}\n" + body + "\n\\end{quote} \\flushnotes"
    if first.startswith("|"):
        rows = [l for l in lines if l.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", l)]
        out = []
        for r in rows:
            cells = [c.strip() for c in r.strip("|").split("|")]
            if any(cells):
                out.append(r" \quad ".join(with_notes(inline(c)) for c in cells) + r" \\")
        return "\\begin{quote}\n" + "\n".join(out) + "\n\\end{quote} \\flushnotes"
    if re.match(r"^\s*([*-]|\d+\.) ", first):
        ordered = bool(re.match(r"^\s*\d+\. ", first))
        items, cur = [], []
        for l in lines:
            if re.match(r"^\s*([*-]|\d+\.) ", l):
                if cur:
                    items.append(" ".join(cur))
                cur = [re.sub(r"^\s*([*-]|\d+\.) ", "", l)]
            else:
                cur.append(l.strip())
        items.append(" ".join(cur))
        env = "enumerate" if ordered else "itemize"
        body = "\n".join(r"\item " + with_notes(inline(i)) for i in items)
        return f"\\begin{{{env}}}\n{body}\n\\end{{{env}}} \\flushnotes"
    return with_notes(inline(" ".join(l.strip() for l in lines))) + r" \flushnotes"


def convert(slug: str) -> str:
    md = unicodedata.normalize("NFC", (ORIGINALS / f"{slug}.md").read_text())
    body = md.split("\n---\n", 1)[1]
    body, defs, orphans = split_footnotes(body)
    # A list or quote that markdownify split with blank lines is still one block for us,
    # but plain blank-line splitting is faithful enough: each block becomes a paragraph.
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", body) if b.strip()]
    out = [convert_block(b, defs) for b in blocks]
    out += [inline(t) + r" \flushnotes" for t in orphans]
    return "\n\n".join(o for o in out if o)


def main(argv):
    if len(argv) != 6:
        sys.exit(__doc__)
    slug, out, title, author, year, url = argv
    header = f"\\post{{{escape_tex(title)}}}{{{escape_tex(author)}}}{{{year}}}{{{url}}}\n\n"
    Path(out).write_text(header + convert(slug) + "\n")
    print(out)


if __name__ == "__main__":
    main(sys.argv[1:])
