#!/usr/bin/env python3
"""Generate a self-contained HTML artifact with compact embedded data."""

import json

def main():
    with open("dashboard/data.json") as f:
        data = json.load(f)

    # Compact format: presidents as arrays, events as arrays
    # President: [number, name, term_start, term_end, is_split, gap_start, gap_end,
    #             term_end_1, term_start_2, term_end_2, events[]]
    # Event: [date, title, description, category_index, importance, score]
    categories = sorted(set(
        ev["category"] for p in data for ev in p["events"]
    ))
    cat_idx = {c: i for i, c in enumerate(categories)}

    compact = []
    for pres in data:
        events = []
        for ev in pres["events"]:
            desc = ev.get("description", "")
            if len(desc) > 100:
                desc = desc[:100] + "…"
            events.append([
                ev["date"],
                ev["title"],
                desc,
                cat_idx[ev["category"]],
                ev["importance"],
                ev["score"],
            ])
        p = [
            pres["number"],
            pres["name"],
            pres["term_start"],
            pres["term_end"],
            1 if pres.get("is_split") else 0,
            pres.get("gap_start", ""),
            pres.get("gap_end", ""),
            pres.get("term_end_1", ""),
            pres.get("term_start_2", ""),
            pres.get("term_end_2", ""),
            events,
        ]
        compact.append(p)

    data_json = json.dumps({"c": categories, "p": compact}, separators=(',', ':'))

    with open("dashboard/index.html") as f:
        html = f.read()

    # Build decoder + inline data
    decoder = f"""
const _RAW = {data_json};
const _CATS = _RAW.c;
const INLINE_DATA = _RAW.p.map(p => ({{
  number: p[0], name: p[1], term_start: p[2], term_end: p[3],
  is_split: !!p[4], gap_start: p[5], gap_end: p[6],
  term_end_1: p[7], term_start_2: p[8], term_end_2: p[9],
  events: p[10].map(e => ({{
    date: e[0], title: e[1], description: e[2],
    category: _CATS[e[3]], importance: e[4], score: e[5]
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
        "// source links removed in artifact mode"
    )

    with open("dashboard/artifact.html", "w") as f:
        f.write(html)

    size_kb = len(html.encode()) / 1024
    print(f"Generated dashboard/artifact.html ({size_kb:.0f} KB)")
    print(f"Data payload: {len(data_json)/1024:.0f} KB")

if __name__ == "__main__":
    main()
