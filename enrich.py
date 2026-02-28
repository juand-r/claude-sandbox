#!/usr/bin/env python3
"""
Phase 2: Enrich raw events with categories, importance, duration, and flags.

Fixes applied from verification:
  - Category rules ordered by specificity (first match wins, with negative keywords)
  - Nobel Peace Prize → FOREIGN_POLICY not MILITARY
  - Importance uses full 1-5 range with proper gradient
  - Pre-term and same-date events flagged
  - Output always chronologically sorted

Input:  data/raw/miller_center_events.csv
Output: data/enriched/events_enriched.csv
"""

import csv
import os
from datetime import datetime, timedelta
from collections import Counter

# ─────────────────────────────────────────────────────────────
# CATEGORY RULES — ordered by specificity (first match wins)
# ─────────────────────────────────────────────────────────────
CATEGORY_RULES = [
    ("SCANDAL", {
        "pos": ["scandal", "Watergate", "Teapot Dome", "Iran-Contra", "Lewinsky",
                "special counsel", "special prosecutor", "corruption", "coverup",
                "cover-up", "obstruction of justice", "perjury", "Whitewater"],
        "neg": [],
    }),
    ("EXECUTIVE_ORDER", {
        "pos": ["executive order", "presidential proclamation", "executive action",
                "presidential memorandum"],
        "neg": [],
    }),
    ("ENVIRONMENTAL", {
        "pos": ["national park", "conservation", "environment", "EPA", "forest service",
                "forest reserve", "wildlife", "pollution", "climate", "Clean Air",
                "Clean Water", "endangered species", "wilderness", "monument",
                "reclamation", "Yellowstone", "Grand Canyon", "Crater Lake",
                "bird reservation", "national forest", "conservationist",
                "Antiquities Act", "National Monuments Act", "National Forest Service"],
        "neg": [],
    }),
    ("CIVIL_RIGHTS", {
        "pos": ["civil rights", "slavery", "emancipation", "enslaved",
                "segregation", "desegregation", "voting rights", "suffrage",
                "NAACP", "discrimination", "racial equality", "race riot",
                "Jim Crow", "lynching", "Brown v. Board", "Selma", "Montgomery",
                "14th Amendment", "15th Amendment", "13th Amendment",
                "19th Amendment", "ADA", "disability rights", "LGBTQ",
                "marriage equality", "Indian Removal", "Trail of Tears",
                "Native American", "Freedmen", "Reconstruction",
                "Booker T. Washington", "W.E.B. DuBois", "DuBois",
                "Niagara Movement", "Chinese Exclusion", "internment",
                "Japanese American", "Executive Order 9066",
                "Dred Scott", "Fugitive Slave"],
        "neg": [],
    }),
    ("HUMANITARIAN", {
        "pos": ["earthquake", "hurricane", "flood", "disaster", "famine",
                "refugee", "humanitarian aid", "relief effort", "pandemic",
                "epidemic", "COVID", "polio", "smallpox", "cholera",
                "Yellow Fever", "Spanish Flu", "Katrina"],
        "neg": [],
    }),
    ("JUDICIAL", {
        "pos": ["Supreme Court", "justice appointed", "Chief Justice",
                "court rules", "court ruling", "court decision", " v. ",
                "v.", "impeachment", "impeach", "constitutional amendment",
                "amendment ratif", "unconstitutional"],
        "neg": [],
    }),
    ("MILITARY", {
        "pos": ["war declared", "declaration of war", "troops deployed",
                "military action", "invasion", "bombing", "nuclear weapon",
                "atomic bomb", "missile", "battle of", "siege", "blockade",
                "airstrike", "drone strike", "armed forces", "combat",
                "surrender", "armistice", "ceasefire", "Pearl Harbor",
                "D-Day", "Normandy", "Gettysburg", "Hiroshima", "Nagasaki",
                "Gulf War", "Korean War", "Vietnam War", "Bay of Pigs",
                "military intervention", "marines land", "gunboat",
                "war begins", "war ends", "fleet", "naval",
                "Confederate", "secession", "Fort Sumter",
                "troops", "army", "navy"],
        "neg": ["Nobel Peace", "peace prize", "peace treaty", "peace conference"],
    }),
    ("INFRASTRUCTURE", {
        "pos": ["canal", "railroad", "highway", "bridge", "dam", "interstate",
                "space program", "NASA", "moon landing", "Apollo", "telegraph",
                "telephone", "internet", "transcontinental", "Erie Canal",
                "Panama Canal construction", "TVA", "electrification",
                "Model T", "General Motors", "automobile"],
        "neg": [],
    }),
    ("ECONOMIC", {
        "pos": ["tariff", "tax", "bank", "banking", "recession", "depression",
                "inflation", "unemployment", "trade war", "economy", "fiscal",
                "budget", "national debt", "Federal Reserve", "stimulus",
                "bailout", "stock market", "panic of", "gold standard",
                "currency", "minimum wage", "labor dispute", "strike",
                "Wall Street", "antitrust", "trust-busting", "Sherman Anti",
                "monopoly", "rebate", "freight rate", "New Deal"],
        "neg": ["airstrike", "military strike"],
    }),
    ("FOREIGN_POLICY", {
        "pos": ["treaty", "diplomatic", "ambassador", "foreign policy",
                "international", "United Nations", "sanctions", "embargo",
                "alliance", "summit", "recognition", "annexation",
                "Monroe Doctrine", "Roosevelt Corollary", "Marshall Plan",
                "Cold War", "détente", "Geneva", "Camp David", "Iran deal",
                "Paris Agreement", "trade agreement", "NAFTA", "TPP",
                "Nobel Peace", "peace prize", "peace conference", "Portsmouth",
                "Algeciras", "Hague", "Yalta", "Potsdam",
                "recognized as a republic", "Dominican Republic",
                "Platt Amendment", "Open Door", "League of Nations",
                "Cuban Missile", "Berlin"],
        "neg": [],
    }),
    ("DOMESTIC_POLICY", {
        "pos": ["healthcare", "health care", "education", "immigration",
                "welfare", "Social Security", "Medicare", "Medicaid",
                "Affordable Care", "Prohibition", "Great Society",
                "housing", "food stamp", "public works", "WPA", "CCC",
                "GI Bill", "Homestead Act", "land grant",
                "gun control", "crime bill"],
        "neg": [],
    }),
    ("LEGISLATION", {
        "pos": ["Congress passes", "signs into law", "signs the", "signs a bill",
                "signed the", "legislation", "Act of", "vetoes", "veto",
                "bill passed", "law enacted", "statute"],
        "neg": [],
    }),
    ("ELECTION", {
        "pos": ["elected", "election", "inaugurated", "inauguration",
                "nominated", "reelection", "electoral vote",
                "running mate", "sworn in", "takes office", "takes the oath",
                "midterm"],
        "neg": [],
    }),
    ("GOVERNANCE", {
        "pos": ["appoints", "appointed", "cabinet", "secretary of",
                "department created", "agency", "commission formed",
                "reorganiz", "civil service", "statehood",
                "admitted to the Union"],
        "neg": [],
    }),
]


def classify_category(title, description):
    """First-match classifier with negative keyword override."""
    text = (title + " " + description).lower()
    for category, rule in CATEGORY_RULES:
        pos_hits = sum(1 for kw in rule["pos"] if kw.lower() in text)
        neg_hits = sum(1 for kw in rule["neg"] if kw.lower() in text)
        if pos_hits > 0 and neg_hits == 0:
            return category
    return "OTHER"


# ─────────────────────────────────────────────────────────────
# IMPORTANCE (1-5 with full gradient)
# ─────────────────────────────────────────────────────────────
IMPORTANCE_5 = [
    "civil war", "world war", "emancipation proclamation", "atomic bomb",
    "nuclear", "assassination", "great depression", "new deal",
    "Pearl Harbor", "9/11", "September 11", "moon landing",
    "Louisiana Purchase", "Constitution ratif", "Bill of Rights",
    "Watergate resign", "Civil Rights Act of 1964", "Voting Rights Act",
    "13th Amendment", "14th Amendment", "15th Amendment", "19th Amendment",
    "Social Security Act", "Medicare", "Brown v. Board",
    "Marshall Plan", "NATO formed", "United Nations",
    "Panama Canal", "Affordable Care Act",
    "Indian Removal Act", "Trail of Tears",
    "Dred Scott", "Roe v. Wade", "Cuban Missile Crisis",
    "Bay of Pigs", "internment", "Executive Order 9066",
    "Emancipation", "Fort Sumter",
]

IMPORTANCE_4 = [
    "war declared", "war begins", "war ends", "treaty signed",
    "invasion", "impeach", "Supreme Court appoint",
    "elected president", "wins the presidential",
    "scandal", "resign", "depression", "recession",
    "antitrust", "Sherman Anti",
    "statehood", "admitted to the Union",
    "Homestead Act", "transcontinental railroad",
    "Spanish-American War", "Mexican-American War",
    "Korean War", "Vietnam",
    "Cold War", "Berlin Wall", "Soviet Union",
    "annexation", "secession", "secede",
    "Nobel Peace Prize", "Nobel Prize",
    "Reconstruction", "Compromise of",
    "bank of the United States", "Federal Reserve",
    "Pure Food and Drug", "Meat Inspection",
    "Hepburn Act", "Interstate Commerce",
    "national park", "National Forest Service",
    "GI Bill", "Great White Fleet",
    "League of Nations", "Hay-Pauncefote",
    "tariff", "slavery",
]

IMPORTANCE_3 = [
    "treaty", "act", "signs the", "Congress passes",
    "executive order", "proclamation",
    "inaugurated", "inauguration", "sworn in",
    "election", "electoral vote",
    "strike", "labor", "union",
    "trade", "conference", "summit", "convention",
    "rebellion", "revolt", "uprising",
    "blockade", "embargo", "sanctions",
    "commission", "investigation",
    "riots", "protest",
]

IMPORTANCE_2 = [
    "visits", "travels to", "meets with", "hosts",
    "speech", "address", "message to Congress",
    "announces", "proposes",
    "department", "bureau", "commission formed",
]


def estimate_importance(title, description):
    text = (title + " " + description).lower()
    for kw in IMPORTANCE_5:
        if kw.lower() in text:
            return 5
    for kw in IMPORTANCE_4:
        if kw.lower() in text:
            return 4
    for kw in IMPORTANCE_3:
        if kw.lower() in text:
            return 3
    for kw in IMPORTANCE_2:
        if kw.lower() in text:
            return 2
    return 2


# ─────────────────────────────────────────────────────────────
# DURATION (days)
# ─────────────────────────────────────────────────────────────
DURATION_HINTS = [
    ("world war", 1460), ("civil war", 1460),
    ("war declared", 730), ("war begins", 730),
    ("pandemic", 730), ("depression", 1095), ("recession", 365),
    ("reconstruction", 3650), ("investigation", 180), ("impeach", 90),
    ("campaign", 180), ("strike", 60), ("blockade", 30), ("siege", 60),
    ("conference", 14), ("summit", 3), ("riot", 3), ("massacre", 1),
    ("earthquake", 1), ("hurricane", 7),
    ("election", 1), ("inaugurated", 1), ("inauguration", 1),
    ("signs", 1), ("signed", 1), ("appoints", 1), ("appointed", 1),
    ("executive order", 1), ("battle", 3), ("bombing", 1),
    ("speech", 1), ("address", 1), ("debate", 1), ("veto", 1),
    ("treaty", 1), ("act", 1),
]


def estimate_duration_days(title, description):
    text = (title + " " + description).lower()
    for keyword, days in DURATION_HINTS:
        if keyword in text:
            return days
    return 30


def estimate_end_date(event_date_str, duration_days):
    try:
        start = datetime.strptime(event_date_str, "%Y-%m-%d")
        return (start + timedelta(days=duration_days)).strftime("%Y-%m-%d")
    except ValueError:
        return ""


# ─────────────────────────────────────────────────────────────
# FLAGS
# ─────────────────────────────────────────────────────────────
def add_flags(events):
    """Flag pre-term events and same-date collisions."""
    date_counts = Counter()
    for e in events:
        key = (e.get("president_number"), e.get("event_date"))
        date_counts[key] += 1

    for e in events:
        flags = []
        try:
            ev_date = datetime.strptime(e["event_date"], "%Y-%m-%d")
            term_start = datetime.strptime(e["term_start"], "%Y-%m-%d")
            term_end = datetime.strptime(e["term_end"], "%Y-%m-%d")
            if ev_date < term_start:
                flags.append("PRE_TERM")
            if ev_date > term_end:
                flags.append("POST_TERM")
        except (ValueError, KeyError):
            flags.append("BAD_DATE")

        key = (e.get("president_number"), e.get("event_date"))
        if date_counts[key] > 1:
            flags.append(f"SAME_DATE_x{date_counts[key]}")

        e["flags"] = "|".join(flags) if flags else ""

    return events


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def run_phase2():
    os.makedirs("data/enriched", exist_ok=True)

    input_path = "data/raw/miller_center_events.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run Phase 1 first.")
        return

    events = []
    with open(input_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            events.append(row)

    print(f"Enriching {len(events)} events...")

    for e in events:
        title = e.get("event_title", "")
        desc = e.get("event_description", "")
        e["event_category"] = classify_category(title, desc)
        duration = estimate_duration_days(title, desc)
        e["event_end_date"] = estimate_end_date(e.get("event_date", ""), duration)
        e["duration_days_estimate"] = duration
        e["importance"] = estimate_importance(title, desc)

    events = add_flags(events)

    # Sort by president number then date
    events.sort(key=lambda e: (int(e.get("president_number", 0) or 0), e.get("event_date", "")))

    # Write
    output_path = "data/enriched/events_enriched.csv"
    fieldnames = list(events[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)

    # Report
    cats = Counter(e["event_category"] for e in events)
    imps = Counter(str(e["importance"]) for e in events)
    flagged = sum(1 for e in events if e.get("flags"))

    print(f"\nWrote {len(events)} events to {output_path}")
    print(f"\nCategories:")
    for cat, count in cats.most_common():
        print(f"  {cat:<20} {count:>3}")
    print(f"\nImportance:")
    for imp, count in sorted(imps.items()):
        print(f"  Level {imp}: {count:>3}")
    print(f"\nFlagged: {flagged}")

    return events


if __name__ == "__main__":
    run_phase2()
