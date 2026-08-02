"""
Checks on the CLICS4 loading layer, run against the real database.

These are not unit tests over mock data. The failure mode that wrecked the
inherited scripts was a join that produced plausible-looking output from real
data, so the checks that matter are the ones that assert against known facts
about the actual database.

    python3 src/test_clics.py
"""

import sys

import clics

FAILURES = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f" -- {detail}" if detail else ""))
    if not condition:
        FAILURES.append(name)


def test_concept_join():
    """The bug that broke the inherited extraction: slug space vs name space."""
    names = clics.load_concept_names()
    check(
        "concept vocabulary is ~1725 concepts",
        1700 <= len(names) <= 1750,
        f"got {len(names)}",
    )
    check("LEG survives the slug round trip", names.get("leg") == "LEG")
    check(
        "multiword concepts slugify correctly",
        clics.slugify("ABSTAIN FROM FOOD") == "abstainfromfood",
    )
    check(
        "parenthesised concepts slugify correctly",
        clics.slugify("DAY (24 HOURS)") == "day24hours",
    )

    stats = clics.load_global_stats()
    check(
        "global stats key on slugs, not names",
        frozenset({"leg", "foot"}) in stats,
    )
    check(
        "no stats entry survives in name space",
        frozenset({"LEG", "FOOT"}) not in stats,
    )


def test_known_family_counts():
    """
    Family counts published in the CLICS4 release, read straight off
    colexifications.csv. If a refactor silently breaks the join again, these
    go to zero rather than staying right.
    """
    stats = clics.load_global_stats()
    expected = {
        ("leg", "foot"): 100,
        ("flesh", "meat"): 105,
        ("do", "make"): 76,
        ("blue", "green"): 70,
        ("woman", "wife"): 59,
        ("moon", "month"): 60,
        ("hear", "listen"): 53,
        ("mountain", "hill"): 84,
    }
    for (a, b), families in expected.items():
        got = stats.get(frozenset({a, b}), {}).get("families")
        check(f"{a.upper()}/{b.upper()} = {families} families", got == families, f"got {got}")


def test_variety_lookup():
    english = clics.varieties_for("stan1293")
    check(
        "English resolves to its 5 varieties",
        english == {"29", "291", "632", "2625", "2760"},
        f"got {sorted(english)}",
    )
    check(
        "friendly names resolve to glottocodes",
        clics.resolve_language("russian") == "russ1263",
    )
    check(
        "raw glottocodes pass through",
        clics.resolve_language("stan1293") == "stan1293",
    )


def test_phonetic_form_detection():
    """Form is orthographic in some CLICS4 varieties and IPA in others."""
    check("bare IPA detected", clics.is_phonetic_form("siː", "s iː"))
    check("dot-separated IPA detected", clics.is_phonetic_form("s.iː", "s iː"))
    check("stress-marked IPA detected", clics.is_phonetic_form("ˈfɒɹɪst", "f ɒ ɹ ɪ s t"))
    check("spelling not mistaken for IPA", not clics.is_phonetic_form("sea", "s iː"))
    check(
        "parentheticals stripped from spellings",
        clics.orthographic_key("wood(s)") == clics.orthographic_key("wood"),
    )


def test_homophone_flag():
    """
    English is the useful test case: it has one orthographic variety among
    five phonetic ones, and a well-known stock of homophones.
    """
    colex = clics.colexifications_in(clics.varieties_for("stan1293"))

    homophones = [("sea", "see"), ("son", "sun"), ("meat", "meet"), ("weak", "week")]
    for a, b in homophones:
        pair = frozenset({a, b})
        if pair not in colex:
            check(f"{a}/{b} flagged as homophone", False, "pair absent from English")
            continue
        check(
            f"{a}/{b} flagged as homophone",
            colex[pair]["form_mismatch"] is True,
            f"got {colex[pair]['form_mismatch']}",
        )

    # Real colexifications, which must not be flagged.
    genuine = [("forest", "wood"), ("askinquire", "askrequest"), ("day24hours", "daynotnight")]
    for a, b in genuine:
        pair = frozenset({a, b})
        if pair not in colex:
            check(f"{a}/{b} not flagged", False, "pair absent from English")
            continue
        check(
            f"{a}/{b} not flagged",
            colex[pair]["form_mismatch"] is not True,
            f"got {colex[pair]['form_mismatch']}",
        )


def test_alternatives_only_flag():
    """
    Spanish variety 12 answers HE, SHE and IT with the single cell
    "él/ ella/ ello", and CLICS4's split of that cell manufactures pronoun
    colexifications Spanish does not have.
    """
    spanish = clics.colexifications_in(clics.varieties_for("stan1288"))

    for a, b in [("he", "she"), ("he", "it"), ("she", "it")]:
        pair = frozenset({a, b})
        check(
            f"Spanish {a}/{b} flagged as an expansion artifact",
            pair in spanish and spanish[pair]["alternatives_only"] is True,
        )

    for a, b in [("flesh", "meat"), ("woman", "wife")]:
        pair = frozenset({a, b})
        check(
            f"Spanish {a}/{b} not flagged",
            pair in spanish and spanish[pair]["alternatives_only"] is False,
        )

    # Known limitation, asserted so it is visible rather than forgotten:
    # Japanese variety 1316 records the single form "kaɾe" under HE, SHE and
    # IT alike. That is a source-wordlist error, and it is structurally
    # identical to a genuine colexification, so no heuristic here can catch it.
    japanese = clics.colexifications_in(clics.varieties_for("nucl1643"))
    check(
        "KNOWN GAP: Japanese he/she survives the filters",
        japanese[frozenset({"he", "she"})]["alternatives_only"] is False,
        "single-form-per-concept errors are undetectable structurally",
    )


def test_asymmetry_direction():
    """The pairs this project is built on must come out asymmetric."""
    english = clics.colexifications_in(clics.varieties_for("stan1293"))
    spanish = clics.colexifications_in(clics.varieties_for("stan1288"))
    russian = clics.colexifications_in(clics.varieties_for("russ1263"))

    check(
        "Spanish colexifies WOMAN/WIFE",
        frozenset({"woman", "wife"}) in spanish,
    )
    check(
        "English distinguishes WOMAN/WIFE",
        frozenset({"woman", "wife"}) not in english,
    )
    check(
        "Russian colexifies LEG/FOOT",
        frozenset({"leg", "foot"}) in russian,
    )
    check(
        "English distinguishes LEG/FOOT",
        frozenset({"leg", "foot"}) not in english,
    )


if __name__ == "__main__":
    for fn in [
        test_concept_join,
        test_known_family_counts,
        test_variety_lookup,
        test_phonetic_form_detection,
        test_homophone_flag,
        test_alternatives_only_flag,
        test_asymmetry_direction,
    ]:
        print(f"\n--- {fn.__name__} ---")
        fn()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        sys.exit(1)
    print("All checks passed.")
