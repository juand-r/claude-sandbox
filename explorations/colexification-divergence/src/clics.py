"""
Loading and querying the CLICS4 database.

CLICS4 ships two tables we care about:

  forms.csv            one row per (language variety, concept, word form).
                       Colexification is visible here as two concepts in the
                       same variety sharing a value in the Segments column.

  colexifications.csv  the aggregated concept-pair graph, with counts of how
                       many varieties, languages, and families attest each pair.

The two tables identify concepts differently, which is the trap that broke the
inherited scripts. forms.csv uses a lowercase slug in Parameter_ID ("leg");
colexifications.csv uses an uppercase name in Source_Concept/Target_Concept
("LEG"). Joining them directly yields zero matches and, because a dict lookup
with a default hides that, zero counts rather than an error. Everything here
works in slug space and calls concept_name() only for display.

Run src/setup_clics4.sh first to fetch the data.
"""

import csv
import re
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

csv.field_size_limit(sys.maxsize)

CLDF_DIR = Path(__file__).resolve().parent.parent / "vendor" / "clics4" / "cldf"
FORMS_FILE = CLDF_DIR / "forms.csv"
COLEX_FILE = CLDF_DIR / "colexifications.csv"
LANGUAGES_FILE = CLDF_DIR / "languages.csv"

# Glottocodes for the languages this project works with. CLICS4 usually holds
# several varieties per language, contributed by different source wordlists.
GLOTTOCODES = {
    "english": "stan1293",
    "spanish": "stan1288",
    "russian": "russ1263",
    "japanese": "nucl1643",
    "german": "stan1295",
    "french": "stan1290",
    "mandarin": "mand1415",
    "korean": "kore1280",
    "turkish": "nucl1301",
    "portuguese": "port1283",
}


def _require_data():
    if not FORMS_FILE.exists() or not COLEX_FILE.exists():
        raise FileNotFoundError(
            f"CLICS4 tables not found under {CLDF_DIR}. Run src/setup_clics4.sh first."
        )


def slugify(concept_name):
    """
    Convert a colexifications.csv concept name to a forms.csv Parameter_ID.

    "ABSTAIN FROM FOOD" -> "abstainfromfood"

    Verified against CLICS4: all 1725 concept names in colexifications.csv
    slugify to distinct slugs, and every one of them is present in forms.csv.
    (forms.csv has 5 extra slugs -- january, june, nextyear, pelican, poet --
    which are concepts that never colexify with anything, so they have no row
    in colexifications.csv.)
    """
    return re.sub(r"[^a-z0-9]", "", concept_name.lower())


def is_phonetic_form(form, segments):
    """
    True when a Form value is a transcription rather than a spelling.

    CLICS4 pools wordlists that disagree about what Form holds, and it does not
    declare which is which. Among the five English varieties: variety 29 spells
    words ("sea"), varieties 291 and 632 give bare IPA ("siː"), and varieties
    2625 and 2760 give dot-separated IPA ("s.iː"). Since Segments is always IPA,
    a Form that reduces to the Segments string is a transcription.

    This matters because the homophone test compares spellings. Run on a
    phonetic variety it compares IPA to IPA, always finds a match, and reports
    every homophone as a genuine colexification -- which is why "sea"/"see"
    slipped through before this check existed.
    """
    normalised = form.replace(".", "").replace(" ", "").replace("ˈ", "").replace("ˌ", "")
    return normalised == segments.replace(" ", "")


def orthographic_key(form):
    """
    Reduce a spelling to a comparable key.

    Parenthesised material is editorial, not part of the word: English variety
    29 records FOREST as "wood(s)" and WOOD as "wood", which is one word with a
    note about plurality, not two spellings.
    """
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\([^)]*\)", "", form.lower()))


def load_concept_names():
    """Return {slug: display name}, e.g. {"abstainfromfood": "ABSTAIN FROM FOOD"}."""
    _require_data()
    names = {}
    with open(COLEX_FILE, newline="") as f:
        for row in csv.DictReader(f):
            for col in ("Source_Concept", "Target_Concept"):
                name = row[col].strip()
                names[slugify(name)] = name
    return names


def varieties_for(glottocode):
    """
    Return the set of CLICS4 language-variety IDs sharing a glottocode.

    A "language" in CLICS4 is really a variety drawn from one source wordlist,
    so standard English is spread over five IDs. Treating them as one language
    means pooling them.
    """
    _require_data()
    ids = set()
    with open(LANGUAGES_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if row["Glottocode"].strip() == glottocode:
                ids.add(row["ID"].strip())
    if not ids:
        raise ValueError(f"No CLICS4 varieties found for glottocode {glottocode!r}")
    return ids


def resolve_language(name_or_glottocode):
    """Accept either a friendly name from GLOTTOCODES or a raw glottocode."""
    key = name_or_glottocode.lower()
    return GLOTTOCODES.get(key, name_or_glottocode)


def colexifications_in(variety_ids):
    """
    Find every concept pair colexified within the given language varieties.

    A pair is colexified when two concepts share a Segments value (the IPA
    transcription) inside a single variety. This mirrors what pyclics itself
    does; it matches on sound, not spelling.

    Returns {frozenset({slug1, slug2}): evidence}, where evidence records:

      varieties        variety IDs in which the pair is colexified
      segments         the shared IPA strings
      forms_by_concept {slug: sorted list of forms as recorded}
      form_mismatch    True  = spelled differently everywhere (likely homophone)
                       False = share a spelling somewhere (likely real)
                       None  = no variety recorded spellings, so we cannot tell
      alternatives_only True when every variety supporting the pair reached it
                       only through concepts that each carry several competing
                       forms (see below)

    form_mismatch is the local homophony signal. If two concepts share a
    pronunciation but are always spelled differently -- English "sea" and "see"
    -- the shared sound is likely an accident of phonological history rather
    than evidence that speakers treat the concepts as one.

    The test only means something in varieties whose Form column is
    orthographic, so phonetic varieties are excluded from it (see
    is_phonetic_form). For languages recorded only phonetically the answer is
    None rather than a guess; the cross-linguistic family count in
    load_global_stats() is the fallback signal there, and it is the better
    signal in general because it does not depend on orthography at all.

    alternatives_only catches a different artifact. Source wordlists sometimes
    answer several concepts with one cell listing alternatives -- Spanish
    variety 12 answers HE, SHE and IT alike with "él/ ella/ ello" -- and CLICS4
    splits that cell into separate forms and attaches all of them to all of the
    concepts. The cross-product then looks exactly like a colexification. It is
    why Spanish appears to colexify HE with SHE, which it does not.

    The signature is that both concepts carry several competing forms in the
    same variety. A real colexification is normally recorded as one shared
    word: Spanish "carne" appears once under FLESH and once under MEAT. So the
    flag fires when every supporting variety has both concepts holding two or
    more distinct pronunciations. That is a heuristic, not a proof -- a
    language really can have synonyms for both halves of a genuine
    colexification -- so it is reported and never silently dropped.
    """
    _require_data()
    variety_ids = set(variety_ids)

    # (variety, segments) -> list of (concept slug, form as recorded)
    groups = defaultdict(list)
    # (variety, concept) -> distinct pronunciations recorded for it, used to
    # spot concepts answered with a list of alternatives rather than one word
    segments_per_concept = defaultdict(set)

    with open(FORMS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            variety = row["Language_ID"].strip()
            if variety not in variety_ids:
                continue
            segments = row["Segments"].strip()
            if not segments:
                continue
            concept = row["Parameter_ID"].strip()
            groups[(variety, segments)].append((concept, row["Form"].strip()))
            segments_per_concept[(variety, concept)].add(segments)

    evidence = defaultdict(
        lambda: {
            "varieties": set(),
            "segments": set(),
            "forms_by_concept": defaultdict(set),
            # Spelling evidence, tallied per variety and only where the Form
            # column actually holds spellings.
            "spelling_shared": 0,
            "spelling_differs": 0,
            # Varieties supporting the pair where at least one of the two
            # concepts was recorded with a single word rather than a list.
            "single_word_support": 0,
        }
    )

    for (variety, segments), entries in groups.items():
        forms_here = defaultdict(set)
        for concept, form in entries:
            forms_here[concept].add(form)
        if len(forms_here) < 2:
            continue

        spellings_here = {
            concept: {
                orthographic_key(f)
                for f in forms
                if not is_phonetic_form(f, segments) and orthographic_key(f)
            }
            for concept, forms in forms_here.items()
        }

        for c1, c2 in combinations(sorted(forms_here), 2):
            ev = evidence[frozenset({c1, c2})]
            ev["varieties"].add(variety)
            ev["segments"].add(segments)
            ev["forms_by_concept"][c1] |= forms_here[c1]
            ev["forms_by_concept"][c2] |= forms_here[c2]

            s1, s2 = spellings_here[c1], spellings_here[c2]
            if s1 and s2:
                if s1 & s2:
                    ev["spelling_shared"] += 1
                else:
                    ev["spelling_differs"] += 1

            both_are_lists = (
                len(segments_per_concept[(variety, c1)]) > 1
                and len(segments_per_concept[(variety, c2)]) > 1
            )
            if not both_are_lists:
                ev["single_word_support"] += 1

    result = {}
    for pair, ev in evidence.items():
        if ev["spelling_shared"]:
            form_mismatch = False
        elif ev["spelling_differs"]:
            form_mismatch = True
        else:
            form_mismatch = None  # no orthographic variety to judge from
        result[pair] = {
            "varieties": sorted(ev["varieties"]),
            "segments": sorted(ev["segments"]),
            "forms_by_concept": {c: sorted(v) for c, v in ev["forms_by_concept"].items()},
            "form_mismatch": form_mismatch,
            "alternatives_only": ev["single_word_support"] == 0,
        }
    return result


def load_global_stats():
    """
    Return {frozenset({slug1, slug2}): {varieties, languages, families}}.

    The family count is the key number for this project. A pair colexified
    across many unrelated families reflects a conceptual link that languages
    keep rediscovering; a pair colexified in one family is more likely an
    accident of that family's sound history. This is the cross-linguistic
    counterpart to the form_mismatch flag, and it does not depend on
    orthography.
    """
    _require_data()
    stats = {}
    with open(COLEX_FILE, newline="") as f:
        for row in csv.DictReader(f):
            pair = frozenset(
                {slugify(row["Source_Concept"]), slugify(row["Target_Concept"])}
            )
            stats[pair] = {
                "varieties": int(row["Variety_Count"]),
                "languages": int(row["Language_Count"]),
                "families": int(row["Family_Count"]),
            }
    return stats
