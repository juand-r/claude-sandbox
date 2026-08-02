"""Extract colexification asymmetries between English and Spanish."""

import csv
import sys
from collections import defaultdict
from itertools import combinations

csv.field_size_limit(sys.maxsize)

FORMS_FILE = "/home/claude/clics4/cldf/forms.csv"
COLEX_FILE = "/home/claude/clics4/cldf/colexifications.csv"
OUT_DIR = "/home/claude/colexdiv/data"

ENGLISH_IDS = {"29", "291", "632", "2625", "2760"}
SPANISH_IDS = {"12", "296", "2594"}


def get_colexifications(lang_ids):
    groups = defaultdict(list)
    with open(FORMS_FILE, "r", newline="") as f:
        for row in csv.DictReader(f):
            lid = row["Language_ID"].strip()
            if lid not in lang_ids:
                continue
            seg = row["Segments"].strip()
            if not seg:
                continue
            groups[(lid, seg)].append(
                (row["Parameter_ID"].strip(), row["Form"].strip())
            )

    colex = set()
    details = defaultdict(list)
    for (lid, seg), entries in groups.items():
        concepts = list(set(e[0] for e in entries))
        if len(concepts) < 2:
            continue
        for c1, c2 in combinations(concepts, 2):
            pair = frozenset({c1, c2})
            colex.add(pair)
            details[pair].append(
                {
                    "lang_id": lid,
                    "segments": seg,
                    "forms": sorted(set(e[1] for e in entries)),
                }
            )
    return colex, details


def load_global():
    data = {}
    with open(COLEX_FILE, "r", newline="") as f:
        for row in csv.DictReader(f):
            pair = frozenset(
                {row["Source_Concept"].strip(), row["Target_Concept"].strip()}
            )
            data[pair] = {
                "fc": int(row["Family_Count"].strip()),
                "lc": int(row["Language_Count"].strip()),
            }
    return data


def rank_and_print(asymmetries, details, global_data, label, lang_label):
    ranked = []
    for pair in asymmetries:
        g = global_data.get(pair, {"fc": 0, "lc": 0})
        c1, c2 = sorted(pair)
        forms = ", ".join(
            sorted(set(f for d in details[pair] for f in d["forms"]))
        )
        ranked.append((g["fc"], g["lc"], c1, c2, forms))
    ranked.sort(reverse=True)

    print(f"\n=== TOP 50 {label} (by global family count) ===")
    print(f"{'C1':<28} {'C2':<28} {'Fam':>4} {'Lng':>5}  {lang_label} form")
    print("-" * 110)
    for fc, lc, c1, c2, forms in ranked[:50]:
        print(f"{c1:<28} {c2:<28} {fc:>4} {lc:>5}  {forms[:40]}")

    tsv_path = f"{OUT_DIR}/{label.lower().replace(' ', '_').replace('-', '_')}.tsv"
    with open(tsv_path, "w") as f:
        f.write(f"concept1\tconcept2\tfamily_count\tlanguage_count\t{lang_label}_forms\n")
        for fc, lc, c1, c2, forms in ranked:
            f.write(f"{c1}\t{c2}\t{fc}\t{lc}\t{forms}\n")
    return ranked


def main():
    print("Loading forms...")
    eng_colex, eng_det = get_colexifications(ENGLISH_IDS)
    spa_colex, spa_det = get_colexifications(SPANISH_IDS)

    print(f"English colexifications: {len(eng_colex)}")
    print(f"Spanish colexifications: {len(spa_colex)}")
    print(f"Shared: {len(eng_colex & spa_colex)}")

    spa_only = spa_colex - eng_colex
    eng_only = eng_colex - spa_colex
    print(f"Spanish-only: {len(spa_only)}")
    print(f"English-only: {len(eng_only)}")

    print("\nLoading global colexification data...")
    gdata = load_global()
    print(f"Global pairs: {len(gdata)}")

    rank_and_print(spa_only, spa_det, gdata, "SPANISH-ONLY", "spanish")
    rank_and_print(eng_only, eng_det, gdata, "ENGLISH-ONLY", "english")

    print(f"\nResults saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()
