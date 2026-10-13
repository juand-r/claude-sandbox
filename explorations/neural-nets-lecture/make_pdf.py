"""Combine the slide screenshots written by tests/pdf.js into neural_nets_<deck>.pdf (one page per slide).

Usage: .venv/bin/python make_pdf.py <1|2>
"""
import sys
from pathlib import Path
from PIL import Image

deck = sys.argv[1]
here = Path(__file__).parent
files = sorted((here / "pdf" / f"slides_{deck}").glob("*.png"))
assert files, "no screenshots: run tests/pdf.js first"
pages = [Image.open(f).convert("RGB") for f in files]
out = here / f"neural_nets_{deck}.pdf"
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=200.0, quality=92)
print(f"wrote {out.name}: {len(pages)} pages, {out.stat().st_size / 1e6:.1f} MB")
