"""Check the PDF links that grapes.sty makes between marks and notes.

Every note (id N) has two marks: one in the text (target grapes-tN) and one
at the start of the note (target grapes-bN). The text mark links to grapes-bN,
the note mark links back to grapes-tN. So a link to grapes-bN must sit where
grapes-tN is (same page, same height), and the reverse.

Checks:
  1. every link points to a destination that exists;
  2. every mark link sits on the same page as its partner target, within
     TOLERANCE points vertically;
  3. (optional) the number of mark links equals --expect-marks.

Usage: python check_links.py FILE.pdf [--expect-marks N]
Exit status 1 on any failure, with one line per problem.
"""
import argparse
import re
import sys

from pypdf import PdfReader

TOLERANCE = 12.0  # points; a mark's link box and its target differ by < 1 line
MARK_DEST = re.compile(r"^grapes-([tb])(\d+)$")


def link_dest_name(annot):
    """Return the named destination of a link annotation, or None."""
    if "/Dest" in annot:
        return str(annot["/Dest"])
    action = annot.get("/A")
    if action is not None and action.get("/S") == "/GoTo":
        return str(action["/D"])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--expect-marks", type=int, default=None)
    args = ap.parse_args()

    reader = PdfReader(args.pdf)
    dests = {}  # name -> (page index, top)
    for name, d in reader.named_destinations.items():
        dests[str(name)] = (reader.get_destination_page_number(d), float(d.top or 0))

    problems = []
    mark_links = 0
    for pageno, page in enumerate(reader.pages):
        for ref in page.get("/Annots", []) or []:
            annot = ref.get_object()
            if annot.get("/Subtype") != "/Link":
                continue
            name = link_dest_name(annot)
            if name is None:
                continue
            if name not in dests:
                problems.append(f"page {pageno + 1}: link to missing destination {name}")
                continue
            m = MARK_DEST.match(name)
            if not m:
                continue  # a cross-reference; existence is all we check
            mark_links += 1
            side, nid = m.groups()
            partner = f"grapes-{'b' if side == 't' else 't'}{nid}"
            if partner not in dests:
                problems.append(f"page {pageno + 1}: {name} has no partner {partner}")
                continue
            ppage, ptop = dests[partner]
            rect_top = float(annot["/Rect"][3])
            if ppage != pageno:
                problems.append(f"page {pageno + 1}: link to {name} is on page "
                                f"{pageno + 1} but {partner} is on page {ppage + 1}")
            elif abs(rect_top - ptop) > TOLERANCE:
                problems.append(f"page {pageno + 1}: link to {name} at y={rect_top:.0f} "
                                f"but {partner} at y={ptop:.0f}")

    if args.expect_marks is not None and mark_links != args.expect_marks:
        problems.append(f"expected {args.expect_marks} mark links, found {mark_links}")

    for p in problems:
        print(p)
    print(f"{args.pdf}: {mark_links} mark links, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
