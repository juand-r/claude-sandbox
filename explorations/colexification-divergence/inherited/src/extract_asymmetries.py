"""
Extract colexification asymmetries between English and Spanish from CLICS4.

For each language, we find all concept pairs that share the same phonological
form (Segments column). Then we find pairs colexified in one language but not
the other.
"""

import csv
from collections import defaultdict
from itertools import combinations

FORMS_FILE = "/home/claude/clics4/cldf/forms.csv"
COLEXIFICATIONS_FILE = "/home/claude/clics4/cldf/colexifications.csv"

# Glottocodes
ENGLISH_GLOTTOCODE = "stan1293"
SPANISH_GLOTTOCODE = "stan1288"

# Language IDs (from languages.csv)
ENGLISH_IDS = {"29", "291", "632", "2625", "2760"}
SPANISH_IDS = {"12", "296", "2594"}


def get_colexifications_for_language(forms_file, lang_ids):
    """
    For a set of language variety IDs, find all concept pairs that share
    the same phonological form (Segments).

    Returns:
        colex: set of frozenset({concept1, concept2}) pairs
        word_for_pair: dict mapping frozenset -> list of (form, segments) tuples
    """
    # Group forms by (language_id, segments)
    form_groups = defaultdict(list)

    with open(forms_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lid = row["Language_ID"].strip()
            if lid not in lang_ids:
                continue
            segments = row["Segments"].strip()
            concept = row["Parameter_ID"].strip()
            form = row["Form"].strip()
            if segments:
                form_groups[(lid, segments)].append((concept, form))

    colex = set()
    word_for_pair = defaultdict(list)

    for (lid, segments), entries in form_groups.items():
        concepts_in_group = list(set(e[0] for e in entries))
        if len(concepts_in_group) < 2:
            continue
        for c1, c2 in combinations(concepts_in_group, 2):
            pair = frozenset({c1, c2})
            colex.add(pair)
            # Find the form string(s)
            forms_used = set(e[1] for e in entries)
            word_for_pair[pair].append({
                "lang_id": lid,
                "segments": segments,
                "forms": forms_used,
                "concepts": (c1, c2),
            })

    return colex, word_for_pair


def load_global_colexification_data(colex_file):
    """Load the global colexification data to get family counts etc."""
    colex_data = {}
    with open(colex_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["Source_Concept"].strip()
            tgt = row["Target_Concept"].strip()
            pair = frozenset({src, tgt})
            colex_data[pair] = {
                "family_count": int(row["Family_Count"]),
                "language_count": int(row["Language_Count"]),
                "variety_count": int(row["Variety_Count"]),
            }
    return colex_data


def main():
    print("Loading forms data...")
    eng_colex, eng_words = get_colexifications_for_language(FORMS_FILE, ENGLISH_IDS)
    spa_colex, spa_words = get_colexifications_for_language(FORMS_FILE, SPANISH_IDS)

    print(f"English colexifications: {len(eng_colex)}")
    print(f"Spanish colexifications: {len(spa_colex)}")
    print(f"Shared: {len(eng_colex & spa_colex)}")

    spa_only = spa_colex - eng_colex
    eng_only = eng_colex - spa_colex

    print(f"Spanish-only colexifications: {len(spa_only)}")
    print(f"English-only colexifications: {len(eng_only)}")

    # Load global data for family counts
    print("\nLoading global colexification data...")
    global_data = load_global_colexification_data(COLEXIFICATIONS_FILE)

    # Rank Spanish-only colexifications by global family count
    # (higher count = more likely polysemy/underspecification, not homophony)
    spa_only_ranked = []
    for pair in spa_only:
        gdata = global_data.get(pair, {})
        family_count = gdata.get("family_count", 0)
        lang_count = gdata.get("language_count", 0)
        c1, c2 = sorted(pair)
        word_info = spa_words[pair]
        forms_str = "; ".join(
            f"{w['forms']} (lang {w['lang_id']})" for w in word_info
        )
        spa_only_ranked.append({
            "concept1": c1,
            "concept2": c2,
            "family_count": family_count,
            "language_count": lang_count,
            "spanish_forms": forms_str,
        })

    spa_only_ranked.sort(key=lambda x: x["family_count"], reverse=True)

    # Similarly for English-only
    eng_only_ranked = []
    for pair in eng_only:
        gdata = global_data.get(pair, {})
        family_count = gdata.get("family_count", 0)
        lang_count = gdata.get("language_count", 0)
        c1, c2 = sorted(pair)
        word_info = eng_words[pair]
        forms_str = "; ".join(
            f"{w['forms']} (lang {w['lang_id']})" for w in word_info
        )
        eng_only_ranked.append({
            "concept1": c1,
            "concept2": c2,
            "family_count": family_count,
            "language_count": lang_count,
            "english_forms": forms_str,
        })

    eng_only_ranked.sort(key=lambda x: x["family_count"], reverse=True)

    # Write results
    print("\n=== TOP 40 SPANISH-ONLY COLEXIFICATIONS (by global family count) ===")
    print(f"{'Concept 1':<25} {'Concept 2':<25} {'Fam':>4} {'Lang':>5}  Spanish word(s)")
    print("-" * 110)
    for item in spa_only_ranked[:40]:
        print(
            f"{item['concept1']:<25} {item['concept2']:<25} "
            f"{item['family_count']:>4} {item['language_count']:>5}  "
            f"{item['spanish_forms'][:50]}"
        )

    print("\n=== TOP 40 ENGLISH-ONLY COLEXIFICATIONS (by global family count) ===")
    print(f"{'Concept 1':<25} {'Concept 2':<25} {'Fam':>4} {'Lang':>5}  English word(s)")
    print("-" * 110)
    for item in eng_only_ranked[:40]:
        print(
            f"{item['concept1']:<25} {item['concept2']:<25} "
            f"{item['family_count']:>4} {item['language_count']:>5}  "
            f"{item['english_forms'][:50]}"
        )

    # Save full results as TSV
    with open("/home/claude/colexdiv/data/spa_only_asymmetries.tsv", "w") as f:
        f.write("concept1\tconcept2\tfamily_count\tlanguage_count\tspanish_forms\n")
        for item in spa_only_ranked:
            f.write(
                f"{item['concept1']}\t{item['concept2']}\t"
                f"{item['family_count']}\t{item['language_count']}\t"
                f"{item['spanish_forms']}\n"
            )

    with open("/home/claude/colexdiv/data/eng_only_asymmetries.tsv", "w") as f:
        f.write("concept1\tconcept2\tfamily_count\tlanguage_count\tenglish_forms\n")
        for item in eng_only_ranked:
            f.write(
                f"{item['concept1']}\t{item['concept2']}\t"
                f"{item['family_count']}\t{item['language_count']}\t"
                f"{item['english_forms']}\n"
            )

    print(f"\nFull results saved to /home/claude/colexdiv/data/")


if __name__ == "__main__":
    main()
