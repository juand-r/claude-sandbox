"""
Extract colexification asymmetries between two languages from CLICS4.

An asymmetry is a concept pair that one language colexifies and the other does
not. These are the predicted sites of forced information divergence: the
distinguishing language cannot render the colexifying language's content
without committing to one concept or the other.

Usage:
    python3 src/extract_asymmetries.py russian english
    python3 src/extract_asymmetries.py spanish english --min-families 10

Writes a TSV per direction to data/, and prints the top rows.

Ranking is by the number of language families that colexify the pair
worldwide. High family counts mean many unrelated languages independently
merge the two concepts, which is evidence of a real conceptual link rather
than an accident of one language's sound history.
"""

import argparse
from pathlib import Path

import clics

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# A pair attested in only a handful of families is more likely coincidence
# than shared meaning. This is the default cutoff for the printed summary;
# the TSV keeps everything so the choice can be revisited.
DEFAULT_MIN_FAMILIES = 5


def build_rows(pairs, evidence, stats, names):
    """Assemble one output row per asymmetric concept pair."""
    rows = []
    for pair in pairs:
        c1, c2 = sorted(pair)
        ev = evidence[pair]
        # Absent from colexifications.csv means no language anywhere colexifies
        # the pair -- which cannot happen for a pair we just observed, unless
        # the concepts fall outside the aggregated graph. Recorded as 0.
        st = stats.get(pair, {"families": 0, "languages": 0, "varieties": 0})
        rows.append(
            {
                "concept1": names.get(c1, c1),
                "concept2": names.get(c2, c2),
                "families": st["families"],
                "languages": st["languages"],
                "varieties": st["varieties"],
                "n_varieties_here": len(ev["varieties"]),
                "likely_homophone": ev["form_mismatch"],
                "alternatives_only": ev["alternatives_only"],
                "segments": " | ".join(ev["segments"][:3]),
                "forms": " | ".join(
                    ",".join(v) for v in ev["forms_by_concept"].values()
                ),
            }
        )
    rows.sort(key=lambda r: (-r["families"], -r["languages"], r["concept1"]))
    return rows


def write_tsv(rows, path):
    columns = [
        "concept1",
        "concept2",
        "families",
        "languages",
        "varieties",
        "n_varieties_here",
        "likely_homophone",
        "alternatives_only",
        "segments",
        "forms",
    ]
    with open(path, "w") as f:
        f.write("\t".join(columns) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in columns) + "\n")


def report(rows, label, min_families, limit=30):
    # likely_homophone is tri-state: True (spelled differently everywhere),
    # False (shares a spelling), or None (nothing to judge from). Only True is
    # grounds for exclusion; None is kept, since absence of evidence about
    # orthography is not evidence of homophony.
    above = [r for r in rows if r["families"] >= min_families]
    kept = [
        r
        for r in above
        if r["likely_homophone"] is not True and not r["alternatives_only"]
    ]
    unjudged = sum(1 for r in kept if r["likely_homophone"] is None)
    dropped_expansion = sum(
        1 for r in above if r["likely_homophone"] is not True and r["alternatives_only"]
    )

    print(f"\n=== {label} ===")
    print(f"{len(rows)} asymmetric pairs total")
    print(f"  {len(rows) - len(above)} below the {min_families}-family threshold")
    print(f"  {len(above) - len(kept) - dropped_expansion} above it but flagged as likely homophones")
    print(f"  {dropped_expansion} above it but flagged as multi-alternative expansions")
    print(f"  {len(kept)} remaining ({unjudged} with no orthographic evidence either way)")

    if not kept:
        return kept

    print(f"\nTop {min(limit, len(kept))} by family count:")
    print(f"{'Concept 1':<24} {'Concept 2':<24} {'Fam':>4} {'Lang':>5}  Form(s)")
    print("-" * 100)
    for r in kept[:limit]:
        print(
            f"{r['concept1'][:23]:<24} {r['concept2'][:23]:<24} "
            f"{r['families']:>4} {r['languages']:>5}  {r['forms'][:34]}"
        )
    return kept


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("lang_a", help="e.g. russian, or a raw glottocode")
    ap.add_argument("lang_b", help="e.g. english, or a raw glottocode")
    ap.add_argument(
        "--min-families",
        type=int,
        default=DEFAULT_MIN_FAMILIES,
        help=f"family-count cutoff for the printed summary (default {DEFAULT_MIN_FAMILIES})",
    )
    args = ap.parse_args()

    DATA_DIR.mkdir(exist_ok=True)

    gc_a = clics.resolve_language(args.lang_a)
    gc_b = clics.resolve_language(args.lang_b)

    print(f"Loading forms for {args.lang_a} ({gc_a}) and {args.lang_b} ({gc_b})...")
    varieties_a = clics.varieties_for(gc_a)
    varieties_b = clics.varieties_for(gc_b)
    print(f"  {args.lang_a}: {len(varieties_a)} varieties")
    print(f"  {args.lang_b}: {len(varieties_b)} varieties")

    colex_a = clics.colexifications_in(varieties_a)
    colex_b = clics.colexifications_in(varieties_b)
    print(f"  {args.lang_a}: {len(colex_a)} colexified pairs")
    print(f"  {args.lang_b}: {len(colex_b)} colexified pairs")
    print(f"  shared: {len(set(colex_a) & set(colex_b))}")

    print("Loading the aggregated concept-pair graph...")
    stats = clics.load_global_stats()
    names = clics.load_concept_names()

    directions = [
        (args.lang_a, colex_a, args.lang_b, colex_b),
        (args.lang_b, colex_b, args.lang_a, colex_a),
    ]
    for src, src_colex, tgt, tgt_colex in directions:
        only = set(src_colex) - set(tgt_colex)
        rows = build_rows(only, src_colex, stats, names)
        label = f"{src.upper()} colexifies, {tgt.upper()} distinguishes"
        report(rows, label, args.min_families)
        path = DATA_DIR / f"asymmetry_{src}_not_{tgt}.tsv"
        write_tsv(rows, path)
        print(f"\nWrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    main()
