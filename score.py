#!/usr/bin/env python3
"""
Phase 4: Score each event on a moral impact scale (-100 to +100).

Approach:
  1. Check for specific well-known events (override list)
  2. Compute a base valence from positive/negative keyword hits
  3. Scale magnitude by the event's importance level (1-5)
  4. Generate a short impact_description

Input:  data/enriched/events_enriched.csv
Output: data/scored/events_scored.csv
"""

import csv
import os
import re
from collections import Counter

# ─────────────────────────────────────────────────────────────
# SPECIFIC EVENT OVERRIDES — well-known events with clear moral weight
# Matched against (title + description), case-insensitive substring
# ─────────────────────────────────────────────────────────────
SPECIFIC_OVERRIDES = [
    # Strongly positive (+70 to +100)
    ("Emancipation Proclamation",           +95, "Freed enslaved people in Confederate states"),
    ("13th Amendment",                       +95, "Abolished slavery in the United States"),
    ("Civil Rights Act of 1964",            +90, "Landmark legislation banning discrimination"),
    ("Voting Rights Act",                   +90, "Protected voting rights for minorities"),
    ("19th Amendment",                       +85, "Granted women the right to vote"),
    ("Brown v. Board",                       +85, "Ended legal school segregation"),
    ("Social Security Act",                 +80, "Created social safety net for elderly and disabled"),
    ("Medicare",                             +75, "Provided healthcare for elderly Americans"),
    ("Affordable Care Act",                 +70, "Expanded healthcare access to millions"),
    ("Marshall Plan",                        +80, "Rebuilt war-torn Europe, prevented famine"),
    ("GI Bill",                              +75, "Provided education and housing for veterans"),
    ("moon landing",                         +70, "Historic achievement in human exploration"),
    ("Apollo 11",                            +70, "First humans on the Moon"),
    ("United Nations",                       +70, "Created framework for international cooperation"),
    ("NATO formed",                          +65, "Built collective defense alliance"),
    ("Louisiana Purchase",                   +75, "Doubled the size of the nation peacefully"),
    ("Bill of Rights",                       +90, "Guaranteed fundamental individual freedoms"),
    ("Constitution ratif",                   +90, "Established the framework of American democracy"),
    ("Clean Air Act",                        +65, "Protected public health from air pollution"),
    ("Clean Water Act",                      +65, "Protected waterways and drinking water"),
    ("Endangered Species",                   +60, "Protected threatened wildlife"),
    ("National Park",                        +55, "Preserved natural lands for the public"),
    ("Homestead Act",                        +55, "Opened land ownership to ordinary citizens"),
    ("14th Amendment",                       +85, "Guaranteed equal protection under law"),
    ("15th Amendment",                       +80, "Prohibited racial discrimination in voting"),
    ("Pure Food and Drug",                   +65, "Protected consumers from unsafe products"),
    ("Meat Inspection Act",                  +60, "Ensured food safety standards"),
    ("TVA",                                  +55, "Brought electricity and development to impoverished region"),
    ("transcontinental railroad",            +60, "Connected the nation coast to coast"),
    ("Erie Canal",                           +55, "Opened trade route boosting economic growth"),
    ("Panama Canal",                         +50, "Major infrastructure achievement, but built with human cost"),
    ("Nobel Peace Prize",                    +60, "Recognized contributions to world peace"),
    ("Lend-Lease",                           +55, "Aided allies fighting fascism"),
    ("peace treaty",                         +45, "Ended armed conflict"),
    ("ceasefire",                            +40, "Stopped active fighting"),
    ("armistice",                            +45, "Ended hostilities"),
    ("marriage equality",                    +75, "Extended marriage rights to same-sex couples"),
    ("ADA",                                  +70, "Protected rights of people with disabilities"),
    ("desegregat",                           +70, "Advanced racial integration"),
    ("Freedmen's Bureau",                    +60, "Aided formerly enslaved people"),

    # Strongly negative (-70 to -100)
    ("Trail of Tears",                      -95, "Forced displacement and death of Native Americans"),
    ("Indian Removal Act",                  -90, "Forced relocation of Native American nations"),
    ("Executive Order 9066",                -90, "Japanese American internment during WWII"),
    ("internment",                          -85, "Imprisoned citizens based on ethnicity"),
    ("Dred Scott",                          -90, "Ruled enslaved people had no legal rights"),
    ("Fugitive Slave",                      -80, "Required return of escaped enslaved people"),
    ("Chinese Exclusion",                   -75, "Banned immigration based on race"),
    ("Hiroshima",                           -70, "Killed ~80,000 civilians with atomic bomb"),
    ("Nagasaki",                            -65, "Second atomic bombing killed ~40,000 civilians"),
    ("My Lai",                              -85, "Massacre of unarmed Vietnamese civilians"),
    ("Watergate",                           -60, "Presidential abuse of power and obstruction"),
    ("Iran-Contra",                         -55, "Secret illegal arms deals"),
    ("Jim Crow",                            -75, "Enforced racial segregation and oppression"),
    ("Kent State",                          -60, "National Guard killed student protesters"),
    ("Abu Ghraib",                          -65, "Torture and abuse of prisoners"),
    ("Alien and Sedition Acts",             -50, "Restricted free speech and immigration"),
    ("Teapot Dome",                         -45, "Government corruption scandal"),
    ("Lewinsky",                            -30, "Presidential scandal and impeachment"),
    ("massacre",                            -70, "Mass killing of people"),
    ("lynching",                            -80, "Racial terrorism and murder"),

    # Moderately negative (-30 to -69)
    ("Fort Sumter",                         -50, "Start of the Civil War"),
    ("secession",                           -45, "States breaking from the Union"),
    ("Panic of",                            -40, "Economic crisis causing widespread suffering"),
    ("Great Depression",                    -60, "Worst economic disaster in US history"),
    ("recession",                           -35, "Economic downturn causing job losses"),
    ("Bay of Pigs",                         -45, "Failed invasion attempt"),
    ("Vietnam War",                         -55, "Prolonged war with heavy casualties"),
    ("corruption",                          -40, "Government corruption"),
    ("obstruction of justice",              -50, "Undermining the legal system"),

    # Moderately positive (+30 to +69)
    ("statehood",                           +40, "Expanded the Union"),
    ("admitted to the Union",               +40, "New state joined the nation"),
    ("antitrust",                           +45, "Broke up harmful monopolies"),
    ("trust-busting",                       +45, "Regulated corporate power"),
    ("Federal Reserve",                     +40, "Stabilized the banking system"),
    ("conservation",                        +50, "Protected natural resources"),
    ("Antiquities Act",                     +50, "Enabled preservation of natural and historic sites"),
    ("land grant",                          +45, "Expanded educational access"),
    ("polio",                               +55, "Addressed public health crisis"),
]

# ─────────────────────────────────────────────────────────────
# VALENCE KEYWORDS — general positive/negative moral indicators
# Each keyword has a weight; total is summed and capped
# ─────────────────────────────────────────────────────────────
POSITIVE_KEYWORDS = [
    # Rights and freedoms
    ("rights", 15), ("freedom", 15), ("liberty", 12), ("equality", 15),
    ("protection", 10), ("reform", 10), ("peace", 12),
    # Constructive actions
    ("established", 8), ("created", 8), ("founded", 8), ("built", 8),
    ("expanded", 8), ("improved", 8), ("strengthened", 8),
    ("aid", 10), ("relief", 10), ("support", 8),
    ("education", 10), ("healthcare", 12), ("safety", 10),
    # Diplomacy
    ("diplomatic", 8), ("alliance", 8), ("cooperation", 10),
    ("agreement", 8), ("recognition", 5), ("negotiate", 8),
    # Progress
    ("progress", 10), ("advancement", 8), ("innovation", 8),
    ("discovery", 8), ("achievement", 8),
]

NEGATIVE_KEYWORDS = [
    # Violence
    ("war", 10), ("killed", 15), ("death", 12), ("died", 10),
    ("attack", 12), ("bombing", 15), ("invasion", 12),
    ("destroyed", 12), ("casualties", 15), ("wounded", 10),
    # Oppression
    ("slavery", 20), ("enslaved", 20), ("oppression", 15),
    ("discrimination", 15), ("segregation", 15), ("persecution", 15),
    ("forced removal", 18), ("removal", 8), ("expulsion", 12),
    # Wrongdoing
    ("scandal", 10), ("corruption", 12), ("coverup", 12),
    ("illegal", 10), ("unconstitutional", 10), ("abuse", 12),
    ("violated", 10), ("fraud", 10),
    # Hardship
    ("depression", 10), ("famine", 12), ("poverty", 10),
    ("crisis", 8), ("collapse", 10), ("panic", 10),
    ("unemployment", 8), ("suffering", 12),
    # Conflict
    ("riot", 8), ("revolt", 8), ("rebellion", 8),
    ("conflict", 8), ("dispute", 5),
]

# Some categories have a baseline moral lean
CATEGORY_BASE = {
    "CIVIL_RIGHTS":     +10,
    "HUMANITARIAN":     +10,
    "ENVIRONMENTAL":    +10,
    "INFRASTRUCTURE":   +8,
    "DOMESTIC_POLICY":  +5,
    "ECONOMIC":          0,
    "LEGISLATION":      +3,
    "FOREIGN_POLICY":    0,
    "JUDICIAL":          0,
    "GOVERNANCE":       +3,
    "ELECTION":          0,
    "MILITARY":         -5,
    "SCANDAL":         -15,
    "EXECUTIVE_ORDER":   0,
    "OTHER":             0,
}

# Importance determines how far the score can go from zero
IMPORTANCE_MAGNITUDE = {
    1: 15,
    2: 30,
    3: 50,
    4: 70,
    5: 90,
}


def check_specific_override(title, description):
    """Check if event matches a specific well-known event.

    Matches against title first (strong signal). Falls back to description
    only for keywords that are unlikely to appear as passing references.
    """
    title_lower = title.lower()
    desc_lower = description.lower()

    # Title match is authoritative — use it
    for keyword, score, desc_text in SPECIFIC_OVERRIDES:
        if keyword.lower() in title_lower:
            return score, desc_text

    # Description-only match: only for broad moral concepts, not specific
    # event names that might appear as passing references.
    # Skip specific event names like "Dred Scott", "Indian Removal Act",
    # "Trail of Tears", etc. — these often appear as context in other events.
    TITLE_ONLY_KEYWORDS = {
        "dred scott", "indian removal act", "trail of tears",
        "lincoln-douglas", "fort sumter", "bay of pigs",
        "watergate", "iran-contra", "teapot dome", "lewinsky",
        "hiroshima", "nagasaki", "my lai", "kent state", "abu ghraib",
        "executive order 9066", "chinese exclusion", "fugitive slave",
        "alien and sedition", "pearl harbor",
    }
    for keyword, score, desc_text in SPECIFIC_OVERRIDES:
        kw_lower = keyword.lower()
        if kw_lower in TITLE_ONLY_KEYWORDS:
            continue
        if kw_lower in desc_lower:
            return score, desc_text

    return None, None


def compute_keyword_valence(text):
    """Sum positive and negative keyword weights."""
    text_lower = text.lower()
    pos_score = sum(w for kw, w in POSITIVE_KEYWORDS if kw.lower() in text_lower)
    neg_score = sum(w for kw, w in NEGATIVE_KEYWORDS if kw.lower() in text_lower)
    return pos_score, neg_score


def generate_description(title, score):
    """Generate a short impact description based on title and score."""
    if score >= 70:
        return f"Highly positive impact: {title}"
    elif score >= 40:
        return f"Positive impact: {title}"
    elif score >= 15:
        return f"Moderately positive impact: {title}"
    elif score > -15:
        return f"Mixed or neutral impact: {title}"
    elif score > -40:
        return f"Moderately negative impact: {title}"
    elif score > -70:
        return f"Negative impact: {title}"
    else:
        return f"Highly negative impact: {title}"


def score_event(event):
    """
    Score a single event on the moral impact scale (-100 to +100).

    Priority:
      1. Specific override for well-known events
      2. Keyword valence + category base, scaled by importance
    """
    title = event.get("event_title", "")
    desc = event.get("event_description", "")
    text = title + " " + desc
    category = event.get("event_category", "OTHER")
    importance = int(event.get("importance", 2) or 2)

    # 1. Check specific overrides first
    override_score, override_desc = check_specific_override(title, desc)
    if override_score is not None:
        return max(-100, min(100, override_score)), override_desc

    # 2. Keyword-based scoring
    pos, neg = compute_keyword_valence(text)

    # Net valence: positive - negative
    net_valence = pos - neg

    # Category baseline
    cat_base = CATEGORY_BASE.get(category, 0)

    # Raw score: category base + net valence
    raw = cat_base + net_valence

    # Scale: importance determines how extreme the score can be
    max_mag = IMPORTANCE_MAGNITUDE.get(importance, 30)

    # Normalize raw into the magnitude range
    # Use a soft scaling: tanh-like capping
    if raw > 0:
        score = min(raw, max_mag)
    elif raw < 0:
        score = max(raw, -max_mag)
    else:
        score = 0

    # Clamp
    score = max(-100, min(100, score))

    # Generate description
    impact_desc = generate_description(title, score)

    return score, impact_desc


def run_phase4():
    os.makedirs("data/scored", exist_ok=True)

    input_path = "data/enriched/events_enriched.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run Phase 2 first.")
        return

    events = []
    with open(input_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            events.append(row)

    if not events:
        print("No events found. Nothing to score.")
        return

    print(f"Scoring {len(events)} events...\n")

    for e in events:
        score, desc = score_event(e)
        e["impact_score"] = score
        e["impact_description"] = desc

    # Write output
    output_path = "data/scored/events_scored.csv"
    fieldnames = list(events[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)

    # Report
    scores = [int(e["impact_score"]) for e in events]
    avg = sum(scores) / len(scores)
    pos = sum(1 for s in scores if s > 0)
    neg = sum(1 for s in scores if s < 0)
    neutral = sum(1 for s in scores if s == 0)

    print(f"Wrote {len(events)} scored events to {output_path}\n")
    print(f"Score distribution:")
    print(f"  Positive (>0):  {pos:>5} ({100*pos/len(scores):.1f}%)")
    print(f"  Neutral  (0):   {neutral:>5} ({100*neutral/len(scores):.1f}%)")
    print(f"  Negative (<0):  {neg:>5} ({100*neg/len(scores):.1f}%)")
    print(f"  Average score:  {avg:>+.1f}")
    print(f"  Min score:      {min(scores):>+d}")
    print(f"  Max score:      {max(scores):>+d}")

    # Show score ranges
    buckets = Counter()
    for s in scores:
        if s <= -70:
            buckets["-100 to -70"] += 1
        elif s <= -40:
            buckets["-69 to -40"] += 1
        elif s <= -15:
            buckets["-39 to -15"] += 1
        elif s < 15:
            buckets["-14 to +14"] += 1
        elif s < 40:
            buckets["+15 to +39"] += 1
        elif s < 70:
            buckets["+40 to +69"] += 1
        else:
            buckets["+70 to +100"] += 1

    print(f"\n  Buckets:")
    for label in ["-100 to -70", "-69 to -40", "-39 to -15", "-14 to +14",
                  "+15 to +39", "+40 to +69", "+70 to +100"]:
        count = buckets.get(label, 0)
        bar = "\u2588" * (count // 10)
        print(f"    {label:>13}: {count:>5} {bar}")

    # Top 5 most positive and negative
    sorted_events = sorted(events, key=lambda e: int(e["impact_score"]))
    print(f"\n  Most negative:")
    for e in sorted_events[:5]:
        print(f"    {int(e['impact_score']):>+4d}  {e['president']}: {e['event_title'][:60]}")
    print(f"\n  Most positive:")
    for e in sorted_events[-5:]:
        print(f"    {int(e['impact_score']):>+4d}  {e['president']}: {e['event_title'][:60]}")

    return events


if __name__ == "__main__":
    run_phase4()
