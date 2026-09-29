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


def emphasis(s: str) -> str:
    """Pair asterisk delimiter runs as CommonMark does (with lenient flanking) and emit
    \\emph / \\textbf.

    Placeholders (\\x00n\\x00) count as ordinary letters. A run of three matched against
    a run of three becomes \\textbf{\\emph{...}}. Unmatched asterisks stay literal."""
    def is_space(c):
        return c == "" or c.isspace()

    # "*text**.*" (an italic run closed, then a stray "**" before final punctuation that is
    # itself italic) is one italic run ending in the punctuation.
    s = re.sub(r"(?<=[^\s*])\*\*(?=[.,;:!?]\*(?!\*))", "", s)
    parts, delims = [], []  # parts: text strings or delimiter dicts
    i = 0
    while i < len(s):
        if s[i] == "*":
            j = i
            while j < len(s) and s[j] == "*":
                j += 1
            prev = s[i - 1] if i > 0 else ""
            nxt = s[j] if j < len(s) else ""
            # Lenient flanking: markdownify writes emphasis from HTML, so a run can close
            # after punctuation ("feeling-*generalized") or open before it ("*.*").
            left = not is_space(nxt)
            right = not is_space(prev)
            d = {"n": j - i, "orig": j - i, "open": left, "close": right, "otags": [], "ctags": []}
            parts.append(d)
            delims.append(d)
            i = j
        else:
            j = s.find("*", i)
            j = len(s) if j < 0 else j
            parts.append(s[i:j])
            i = j
    k = 0
    while k < len(delims):
        c = delims[k]
        if not c["close"] or c["n"] == 0:
            k += 1
            continue
        found = None
        for o in range(k - 1, -1, -1):
            op = delims[o]
            if not op["open"] or op["n"] == 0:
                continue
            if (op["close"] or c["open"]) and (op["orig"] + c["orig"]) % 3 == 0 \
                    and not (op["orig"] % 3 == 0 and c["orig"] % 3 == 0):
                continue
            found = o
            break
        if found is None:
            k += 1
            continue
        op = delims[found]
        if op["n"] >= 3 and c["n"] >= 3:
            use, otag, ctag = 3, r"\textbf{\emph{", "}}"
        elif op["n"] >= 2 and c["n"] >= 2:
            use, otag, ctag = 2, r"\textbf{", "}"
        else:
            use, otag, ctag = 1, r"\emph{", "}"
        op["n"] -= use
        c["n"] -= use
        op["otags"].append(otag)
        c["ctags"].append(ctag)
        for mid in delims[found + 1:k]:
            mid["open"] = mid["close"] = False  # delimiters inside the span become literal
        # stay on this closer if it has asterisks left
    out = []
    for p in parts:
        if isinstance(p, str):
            out.append(p)
        else:
            # closing tags first (inner-most matched first), then leftover literal
            # asterisks, then opening tags (inner-most last).
            out.append("".join(p["ctags"]) + "*" * p["n"] + "".join(reversed(p["otags"])))
    return "".join(out)


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

    def link_text(self, md: str) -> str:
        """Link text that is itself a URL is set with \\nolinkurl, so it can break."""
        pieces = md.split()
        if pieces and re.match(r"(https?://|www\.)", pieces[0]) and \
                all(re.search(r"[./]|-$", p) for p in pieces):
            # A URL as link text, possibly broken by a space after a hyphen in the source.
            return " ".join(r"\nolinkurl{" + escape_url(p) + "}" for p in pieces)
        return self.nested(md)

    def nested(self, md: str) -> str:
        """Convert link text. It shares this converter's placeholders, because escapes in
        the text were already replaced by placeholders before links are matched."""
        inner = Inline()
        inner.store = self.store
        return inner.convert(md)

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
                    lambda m: self.protect(r"\href{" + escape_url(m.group(2)) + "}{" + self.link_text(m.group(1)) + "}"), md)
        # Bare URLs in running text (links and autolinks are already protected): \url{}
        # lets LaTeX break them at the margin.
        md = re.sub(r"https?://(?:[^\s<>\]\x00]|\x00\d+\x00)+", lambda m: self.bare_url(m.group(0)), md)
        md = escape_tex(md)
        # Long runs of words joined by slashes ("atheist/libertarian/technophile/...") may
        # break after a slash; \slash{} allows that and prints "/".
        md = re.sub(r"(?<![\w/])[A-Za-z][\w'-]*(?:/[\w'-]+){2,}",
                    lambda m: m.group(0).replace("/", r"\slash{}") if len(m.group(0)) > 20 else m.group(0), md)
        # Escaped literal asterisks were protected above, so every remaining asterisk is
        # an emphasis delimiter. Pair them by the CommonMark rules (emphasis()).
        md = emphasis(md)
        return self.restore(md)

    def bare_url(self, url: str) -> str:
        """Wrap a bare URL; trailing sentence punctuation stays outside."""
        m = re.match(r"(.*?)([.,;:!?)\]*]*)$", url)
        core, tail = m.group(1), m.group(2)
        if tail.startswith(")") and core.count("(") > core.count(")"):
            core, tail = core + ")", tail[1:]  # a balanced parenthesis belongs to the URL
        # Placeholders inside the URL are Markdown escapes (\_ and the like): take the raw
        # character back. Any other placeholder ends the URL.
        raw = {v: k for k, v in TEX_ESCAPES.items()}
        pieces, rest = [], ""
        for tok in re.split(r"(\x00\d+\x00)", core):
            if rest:
                rest += tok
            elif re.fullmatch(r"\x00\d+\x00", tok):
                val = self.store[int(tok[1:-1])]
                if val in raw or len(val) == 1:
                    pieces.append(raw.get(val, val))
                else:
                    rest = tok
            else:
                pieces.append(tok)
        core, tail = "".join(pieces), rest + tail
        return self.protect(r"\url{" + escape_url(core) + "}") + tail


def inline(md: str) -> str:
    return Inline().convert(md)


def split_footnotes(body: str):
    """Pull out '[n](#fnNxK-bk)text' definitions and replace in-text markers with \\cauthor."""
    defs = {}
    kept = []
    last = None  # the footnote whose definition was seen last, for multi-paragraph footnotes
    for line in body.split("\n"):
        m = re.match(r"^\[(\d+)\]\(#(fn[^)]*)-bk\)\s*(.*)$", line)
        if m:
            last = m.group(2)
            defs[last] = m.group(3)
        elif last is not None and line.strip():
            # A paragraph after a footnote definition continues that footnote.
            defs[last] += "\n\n" + line
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
    if re.match(r"^###### ", first):
        # An unnumbered level-6 heading continues the author's numbered notes: plain text.
        return with_notes(inline(re.sub(r"^######\s*", "", " ".join(l.strip() for l in lines)))) + r" \flushnotes"
    if re.match(r"^######\s*$", first) or re.match(r"^---+$", first):
        return ""  # empty heading or horizontal rule: layout only
    if first.startswith(">"):
        paras, cur = [], []
        for l in lines:
            l = re.sub(r"^>\s?", "", l)
            if re.match(r"^-{3,}\s*$", l):
                l = ""  # horizontal rule inside a quote: layout only, as at top level
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
        # "{}" keeps an item that begins with "[" from being read as \item's optional label.
        body = "\n".join(r"\item " + ("{}" if i.startswith("[") else "") + with_notes(inline(i)) for i in items)
        return f"\\begin{{{env}}}\n{body}\n\\end{{{env}}} \\flushnotes"
    return with_notes(inline(" ".join(l.strip() for l in lines))) + r" \flushnotes"


def convert(slug: str) -> str:
    md = unicodedata.normalize("NFC", (ORIGINALS / f"{slug}.md").read_text())
    body = md.split("\n---\n", 1)[1]
    body, defs, orphans = split_footnotes(body)
    # A list or quote that markdownify split with blank lines is still one block for us,
    # but plain blank-line splitting is faithful enough: each block becomes a paragraph.
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", body) if b.strip()]
    # A quote that starts right after a text line, with no blank line between them
    # ("Previously:" then "> ..."), is its own block.
    split = []
    for b in blocks:
        cur = []
        for line in b.split("\n"):
            if line.startswith(">") and cur and not cur[-1].startswith(">"):
                split.append("\n".join(cur))
                cur = []
            cur.append(line)
        split.append("\n".join(cur))
    blocks = split
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
