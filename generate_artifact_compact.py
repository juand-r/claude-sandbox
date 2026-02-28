#!/usr/bin/env python3
"""Generate a compact self-contained HTML artifact (~150KB).
Drops descriptions to minimize size for sharing."""

import json

def main():
    with open("dashboard/data.json") as f:
        data = json.load(f)

    categories = sorted(set(ev["category"] for p in data for ev in p["events"]))
    cat_idx = {c: i for i, c in enumerate(categories)}

    compact = []
    for pres in data:
        events = []
        for ev in pres["events"]:
            t = ev["title"][:50]
            events.append([ev["date"], t, cat_idx[ev["category"]], ev["importance"], ev["score"]])
        p = [pres["number"], pres["name"], pres["term_start"], pres["term_end"],
             1 if pres.get("is_split") else 0,
             pres.get("gap_start", ""), pres.get("gap_end", ""),
             pres.get("term_end_1", ""), pres.get("term_start_2", ""), pres.get("term_end_2", ""),
             events]
        compact.append(p)

    data_json = json.dumps({"c": categories, "p": compact}, separators=(",", ":"))

    with open("dashboard/index.html") as f:
        html = f.read()

    # Decoder that maps compact arrays back to objects (no description field)
    decoder = f"""
const _RAW = {data_json};
const _CATS = _RAW.c;
const INLINE_DATA = _RAW.p.map(p => ({{
  number: p[0], name: p[1], term_start: p[2], term_end: p[3],
  is_split: !!p[4], gap_start: p[5], gap_end: p[6],
  term_end_1: p[7], term_start_2: p[8], term_end_2: p[9],
  events: p[10].map(e => ({{
    date: e[0], title: e[1], description: '',
    category: _CATS[e[2]], importance: e[3], score: e[4]
  }}))
}}));
"""

    old_fetch = """async function loadData() {
  const resp = await fetch('data.json');
  DATA = await resp.json();"""

    new_fetch = """async function loadData() {
  DATA = INLINE_DATA;"""

    html = html.replace(old_fetch, decoder + "\n" + new_fetch)
    html = html.replace(
        "if (bp.event.source) window.open(bp.event.source, '_blank');",
        "// source links removed in compact mode"
    )

    with open("dashboard/artifact_compact.html", "w") as f:
        f.write(html)

    size_kb = len(html.encode()) / 1024
    print(f"Generated dashboard/artifact_compact.html ({size_kb:.0f} KB)")

if __name__ == "__main__":
    main()
