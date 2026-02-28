#!/usr/bin/env python3
"""Generate JSON data for the heatmap dashboard."""

import csv
import json

def main():
    with open("data/scored/events_scored.csv", encoding="utf-8") as f:
        events = list(csv.DictReader(f))

    # Group by president number
    presidents = {}
    for e in events:
        pnum = int(e["president_number"])
        if pnum not in presidents:
            presidents[pnum] = {
                "number": pnum,
                "name": e["president"],
                "term_start": e["term_start"],
                "term_end": e["term_end"],
                "events": [],
            }
        presidents[pnum]["events"].append({
            "date": e["event_date"],
            "title": e["event_title"],
            "description": e["event_description"],
            "category": e["event_category"],
            "importance": int(e["importance"]),
            "score": int(e["impact_score"]),
            "impact": e["impact_description"],
            "source": e["source_url"],
        })

    # Handle Cleveland's two terms
    if 22 in presidents and 24 in presidents:
        presidents[22]["term_end_1"] = presidents[22]["term_end"]
        presidents[22]["term_start_2"] = presidents[24]["term_start"]
        presidents[22]["term_end_2"] = presidents[24]["term_end"]
        # Merge events from term 24 into 22
        presidents[22]["events"].extend(presidents[24]["events"])
        presidents[22]["events"].sort(key=lambda e: e["date"])
        presidents[22]["is_split"] = True
        presidents[22]["gap_start"] = presidents[22]["term_end"]
        presidents[22]["gap_end"] = presidents[24]["term_start"]
        del presidents[24]

    data = sorted(presidents.values(), key=lambda p: p["number"])
    with open("dashboard/data.json", "w") as f:
        json.dump(data, f, indent=1)

    total = sum(len(p["events"]) for p in data)
    print(f"Generated dashboard/data.json: {len(data)} presidents, {total} events")

if __name__ == "__main__":
    main()
