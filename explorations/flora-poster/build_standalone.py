"""Turn a canvas artboard (.dc.html) into a standalone HTML page that prints at its exact size.

Usage:  python build_standalone.py canvas/A0-portrait.dc.html poster-a0.html 841mm 1189mm

What it does:
- drops the canvas runtime (<script src="./support.js">) and the component script block,
- moves the <helmet> contents into <head> and unwraps <x-dc>,
- points uploaded-asset URLs (/_blob/<id>) at the local files in assets/,
- adds an @page rule for the given print size.
"""
import re
import sys
from pathlib import Path

# Uploaded canvas assets -> local copies (see assets/).
BLOBS = {
    "ba4100fb1f251a7230a9393a778f8d2b": "assets/fig5-crop.png",
    "f179bf959bb7fc2b64d9046eb499ecf0": "assets/qr-paper.png",
    "ea560a35bc7802f4fcb88602b835583d": "assets/qr-code.png",
}


def build(src: str, page_w: str, page_h: str) -> str:
    s = src.replace('<script src="./support.js"></script>', "")
    helmet = re.search(r"<helmet>(.*?)</helmet>", s, re.S)
    if helmet is None:
        raise ValueError("no <helmet> block found")
    s = s.replace(helmet.group(0), "").replace("</head>", helmet.group(1) + "</head>")
    s = s.replace("<x-dc>", "<div>").replace("</x-dc>", "</div>")
    s = re.sub(r'<script type="text/x-dc".*?</script>\n', "", s, flags=re.S)
    for blob, path in BLOBS.items():
        s = s.replace(f"/_blob/{blob}", path)
    leftover = re.findall(r"/_blob/[0-9a-f]+", s)
    if leftover:
        raise ValueError(f"unmapped assets: {leftover}")
    return s.replace("<style>", f"<style>\n@page{{size:{page_w} {page_h};margin:0}}", 1)


if __name__ == "__main__":
    src, out, page_w, page_h = sys.argv[1:5]
    Path(out).write_text(build(Path(src).read_text(), page_w, page_h))
