"""Combine the slide screenshots written by tests/pdf.js into neural_nets_<deck>.pdf (one page per slide),
or, with "steps", into neural_nets_<deck>_steps.pdf (one page per step).

Usage: .venv/bin/python make_pdf.py <1|2> [steps]
"""
import sys
from pathlib import Path
from PIL import Image

deck = sys.argv[1]
every = len(sys.argv) > 2 and sys.argv[2] == "steps"
here = Path(__file__).parent
# the names sort in slide order, then step order (steps are single digits)
files = sorted((here / "pdf" / f"{'steps' if every else 'slides'}_{deck}").glob("*.png"))
assert files, "no screenshots: run tests/pdf.js first"
STEPS_WIDTH = 2400   # the step-by-step PDF has about three times the pages, so its pages are smaller
pages = [Image.open(f).convert("RGB") for f in files]
if every:
    pages = [im.resize((STEPS_WIDTH, round(im.height * STEPS_WIDTH / im.width)), Image.LANCZOS) for im in pages]
out = here / f"neural_nets_{deck}{'_steps' if every else ''}.pdf"
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=200.0, quality=92)
print(f"wrote {out.name}: {len(pages)} pages, {out.stat().st_size / 1e6:.1f} MB")
