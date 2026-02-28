#!/usr/bin/env python3
"""
Phase 3: Verify integrity of the enriched dataset.

Checks:
  - All required fields populated
  - Date parsing and bounds
  - Chronological ordering within each president
  - Category and importance distributions
  - Per-president event counts
  - Flagged issues summary
  - Content spot checks (short descriptions, empty titles, valid URLs)

Input:  data/enriched/events_enriched.csv
Output: prints report to stdout (no file output)
"""

import csv
import os
from datetime import datetime
from collections import Counter, defaultdict


def load(path):
    events = []
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            events.append(row)
    return events


def run_verification():
    input_path = "data/enriched/events_enriched.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run Phases 1-2 first.")
        return

    events = load(input_path)
    errors = 0
    warnings = 0

    def err(msg):
        nonlocal errors
        errors += 1
        print(f"  ✗ {msg}")

    def warn(msg):
        nonlocal warnings
        warnings += 1
        print(f"  ⚠ {msg}")

    def ok(msg):
        print(f"  ✓ {msg}")

    # ── 1. BASIC INTEGRITY ──
    print("=" * 70)
    print("1. FIELD INTEGRITY")
    print("=" * 70)

    required = ["president", "president_number", "term_start", "term_end",
                 "event_date", "event_title", "event_description",
                 "event_category", "source_url", "source_name"]
    for field in required:
        empty = sum(1 for e in events if not str(e.get(field, "")).strip())
        if empty:
            err(f"{field}: {empty} empty values")
        else:
            ok(f"{field}: all populated")

    # impact fields: blank in enriched data, filled in scored data
    scored_path = "data/scored/events_scored.csv"
    scored_exists = os.path.exists(scored_path)
    for field in ["impact_score", "impact_description"]:
        filled = sum(1 for e in events if str(e.get(field, "")).strip())
        if filled:
            if scored_exists:
                ok(f"{field}: {filled} populated (scoring complete)")
            else:
                warn(f"{field}: {filled} unexpectedly filled (should be blank for later)")
        else:
            ok(f"{field}: all blank (correct — for later scoring)")

    print(f"\n  Total rows: {len(events)}")

    # ── 2. DATE CHECKS ──
    print("\n" + "=" * 70)
    print("2. DATE INTEGRITY")
    print("=" * 70)

    bad_dates = []
    for e in events:
        try:
            datetime.strptime(e["event_date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            bad_dates.append(e.get("event_date", "MISSING"))

    if bad_dates:
        err(f"{len(bad_dates)} unparseable dates: {bad_dates[:5]}")
    else:
        ok(f"All {len(events)} dates parse correctly (YYYY-MM-DD)")

    # Check chronological order within each president
    by_pres = defaultdict(list)
    for e in events:
        by_pres[int(e.get("president_number", 0) or 0)].append(e)

    out_of_order = 0
    for pnum, pevents in sorted(by_pres.items()):
        dates = []
        for e in pevents:
            try:
                dates.append(datetime.strptime(e["event_date"], "%Y-%m-%d"))
            except ValueError:
                pass
        for i in range(len(dates) - 1):
            if dates[i] > dates[i + 1]:
                out_of_order += 1

    if out_of_order:
        err(f"{out_of_order} out-of-order events found")
    else:
        ok("All events chronologically sorted within each president")

    # ── 3. PER-PRESIDENT COUNTS ──
    print("\n" + "=" * 70)
    print("3. PER-PRESIDENT EVENT COUNTS")
    print("=" * 70)

    pres_counts = Counter()
    pres_names = {}
    for e in events:
        pnum = int(e.get("president_number", 0) or 0)
        pres_counts[pnum] += 1
        pres_names[pnum] = e["president"]

    very_few = []
    print(f"  {'#':>3} {'President':<30} {'Events':>6}")
    print(f"  {'-'*3} {'-'*30} {'-'*6}")
    for pnum in sorted(pres_counts.keys()):
        count = pres_counts[pnum]
        name = pres_names.get(pnum, "?")
        flag = ""
        if count < 3:
            flag = " ← very few"
            very_few.append((pnum, name, count))
        print(f"  {pnum:>3} {name:<30} {count:>6}{flag}")

    # Check for missing president numbers
    expected = set(range(1, 47))
    # 24 is Cleveland's second term — may or may not have events depending
    # on whether the page had events in that date range
    actual = set(pres_counts.keys())
    missing = expected - actual
    if missing:
        warn(f"Missing president numbers: {sorted(missing)}")
    else:
        ok(f"All expected president numbers present")

    if very_few:
        for pnum, name, count in very_few:
            warn(f"#{pnum} {name} has only {count} events")

    total_pres = len(pres_counts)
    avg_events = len(events) / total_pres if total_pres else 0
    print(f"\n  Presidents: {total_pres}")
    print(f"  Total events: {len(events)}")
    print(f"  Average events/president: {avg_events:.1f}")

    # ── 4. CATEGORIES ──
    print("\n" + "=" * 70)
    print("4. CATEGORY DISTRIBUTION")
    print("=" * 70)

    cats = Counter(e["event_category"] for e in events)
    for cat, count in cats.most_common():
        pct = count / len(events) * 100
        bar = "█" * max(1, int(pct / 2))
        print(f"  {cat:<20} {count:>4} ({pct:>5.1f}%) {bar}")

    if "OTHER" in cats and cats["OTHER"] / len(events) > 0.15:
        warn(f"OTHER category is {cats['OTHER']/len(events)*100:.1f}% — classifier may need tuning")
    else:
        ok(f"OTHER category at {cats.get('OTHER', 0)/len(events)*100:.1f}% (acceptable)")

    # ── 5. IMPORTANCE ──
    print("\n" + "=" * 70)
    print("5. IMPORTANCE DISTRIBUTION")
    print("=" * 70)

    imps = Counter(str(e["importance"]) for e in events)
    for imp in ["1", "2", "3", "4", "5"]:
        count = imps.get(imp, 0)
        pct = count / len(events) * 100
        bar = "█" * max(0, int(pct / 2))
        print(f"  Level {imp}: {count:>4} ({pct:>5.1f}%) {bar}")

    used_levels = set(imps.keys())
    if len(used_levels) < 3:
        warn(f"Only {len(used_levels)} importance levels used — needs more gradient")
    else:
        ok(f"{len(used_levels)} importance levels used")

    # ── 6. FLAGS ──
    print("\n" + "=" * 70)
    print("6. FLAGGED EVENTS")
    print("=" * 70)

    flagged = [e for e in events if e.get("flags", "").strip()]
    flag_types = Counter()
    for e in flagged:
        for f in e["flags"].split("|"):
            if f.strip():
                flag_types[f.strip()] += 1

    if flagged:
        print(f"  Total flagged: {len(flagged)}")
        for ftype, count in flag_types.most_common():
            print(f"    {ftype}: {count}")
    else:
        ok("No flagged events")

    # ── 7. CONTENT SPOT CHECKS ──
    print("\n" + "=" * 70)
    print("7. CONTENT CHECKS")
    print("=" * 70)

    short_descs = [e for e in events if len(e.get("event_description", "")) < 20]
    if short_descs:
        warn(f"{len(short_descs)} events with very short descriptions (<20 chars)")
        for e in short_descs[:5]:
            print(f"    '{e['event_title']}' — {len(e['event_description'])} chars")
    else:
        ok("All descriptions ≥20 chars")

    empty_titles = [e for e in events if not e.get("event_title", "").strip()]
    if empty_titles:
        err(f"{len(empty_titles)} empty titles")
    else:
        ok("No empty titles")

    bad_urls = [e for e in events if not e.get("source_url", "").startswith("http")]
    if bad_urls:
        err(f"{len(bad_urls)} invalid source URLs")
    else:
        ok("All source URLs valid")

    # Check for extremely long descriptions (possible parsing artifacts)
    long_descs = [e for e in events if len(e.get("event_description", "")) > 2000]
    if long_descs:
        warn(f"{len(long_descs)} events with very long descriptions (>2000 chars)")
    else:
        ok("No excessively long descriptions")

    # ── SUMMARY ──
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Errors:   {errors}")
    print(f"  Warnings: {warnings}")
    if errors == 0:
        print(f"  ✓ Dataset passes integrity checks")
    else:
        print(f"  ✗ {errors} errors need fixing")


if __name__ == "__main__":
    run_verification()
