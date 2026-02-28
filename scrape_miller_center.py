#!/usr/bin/env python3
"""
Phase 1: Scrape Miller Center Key Events for all US Presidents.

Fetches https://millercenter.org/president/{slug}/key-events for each president,
parses dated events from the page text, and writes raw CSV.

Output: data/raw/miller_center_events.csv
"""

import requests
import re
import csv
import os
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────
# President metadata
# ─────────────────────────────────────────────────────────────
PRESIDENTS = [
    {"slug": "washington",          "name": "George Washington",        "number": 1,  "term_start": "1789-04-30", "term_end": "1797-03-04"},
    {"slug": "adams",              "name": "John Adams",               "number": 2,  "term_start": "1797-03-04", "term_end": "1801-03-04"},
    {"slug": "jefferson",          "name": "Thomas Jefferson",          "number": 3,  "term_start": "1801-03-04", "term_end": "1809-03-04"},
    {"slug": "madison",            "name": "James Madison",             "number": 4,  "term_start": "1809-03-04", "term_end": "1817-03-04"},
    {"slug": "monroe",             "name": "James Monroe",              "number": 5,  "term_start": "1817-03-04", "term_end": "1825-03-04"},
    {"slug": "jqadams",            "name": "John Quincy Adams",         "number": 6,  "term_start": "1825-03-04", "term_end": "1829-03-04"},
    {"slug": "jackson",            "name": "Andrew Jackson",            "number": 7,  "term_start": "1829-03-04", "term_end": "1837-03-04"},
    {"slug": "martin-van-buren",   "name": "Martin Van Buren",          "number": 8,  "term_start": "1837-03-04", "term_end": "1841-03-04"},
    {"slug": "harrison",           "name": "William Henry Harrison",    "number": 9,  "term_start": "1841-03-04", "term_end": "1841-04-04"},
    {"slug": "john-tyler",         "name": "John Tyler",                "number": 10, "term_start": "1841-04-04", "term_end": "1845-03-04"},
    {"slug": "polk",               "name": "James K. Polk",             "number": 11, "term_start": "1845-03-04", "term_end": "1849-03-04"},
    {"slug": "zachary-taylor",     "name": "Zachary Taylor",            "number": 12, "term_start": "1849-03-04", "term_end": "1850-07-09"},
    {"slug": "fillmore",           "name": "Millard Fillmore",          "number": 13, "term_start": "1850-07-09", "term_end": "1853-03-04"},
    {"slug": "pierce",             "name": "Franklin Pierce",           "number": 14, "term_start": "1853-03-04", "term_end": "1857-03-04"},
    {"slug": "buchanan",           "name": "James Buchanan",            "number": 15, "term_start": "1857-03-04", "term_end": "1861-03-04"},
    {"slug": "lincoln",            "name": "Abraham Lincoln",           "number": 16, "term_start": "1861-03-04", "term_end": "1865-04-15"},
    {"slug": "johnson",            "name": "Andrew Johnson",            "number": 17, "term_start": "1865-04-15", "term_end": "1869-03-04"},
    {"slug": "grant",              "name": "Ulysses S. Grant",          "number": 18, "term_start": "1869-03-04", "term_end": "1877-03-04"},
    {"slug": "hayes",              "name": "Rutherford B. Hayes",       "number": 19, "term_start": "1877-03-04", "term_end": "1881-03-04"},
    {"slug": "garfield",           "name": "James A. Garfield",         "number": 20, "term_start": "1881-03-04", "term_end": "1881-09-19"},
    {"slug": "arthur",             "name": "Chester A. Arthur",         "number": 21, "term_start": "1881-09-19", "term_end": "1885-03-04"},
    {"slug": "cleveland",          "name": "Grover Cleveland",          "number": 22, "term_start": "1885-03-04", "term_end": "1889-03-04"},
    {"slug": "bharrison",          "name": "Benjamin Harrison",         "number": 23, "term_start": "1889-03-04", "term_end": "1893-03-04"},
    {"slug": "mckinley",           "name": "William McKinley",          "number": 25, "term_start": "1897-03-04", "term_end": "1901-09-14"},
    {"slug": "theodore-roosevelt", "name": "Theodore Roosevelt",        "number": 26, "term_start": "1901-09-14", "term_end": "1909-03-04"},
    {"slug": "taft",               "name": "William Howard Taft",       "number": 27, "term_start": "1909-03-04", "term_end": "1913-03-04"},
    {"slug": "wilson",             "name": "Woodrow Wilson",            "number": 28, "term_start": "1913-03-04", "term_end": "1921-03-04"},
    {"slug": "harding",            "name": "Warren G. Harding",         "number": 29, "term_start": "1921-03-04", "term_end": "1923-08-02"},
    {"slug": "coolidge",           "name": "Calvin Coolidge",           "number": 30, "term_start": "1923-08-02", "term_end": "1929-03-04"},
    {"slug": "hoover",             "name": "Herbert Hoover",            "number": 31, "term_start": "1929-03-04", "term_end": "1933-03-04"},
    {"slug": "fdroosevelt",        "name": "Franklin D. Roosevelt",     "number": 32, "term_start": "1933-03-04", "term_end": "1945-04-12"},
    {"slug": "truman",             "name": "Harry S. Truman",           "number": 33, "term_start": "1945-04-12", "term_end": "1953-01-20"},
    {"slug": "eisenhower",         "name": "Dwight D. Eisenhower",      "number": 34, "term_start": "1953-01-20", "term_end": "1961-01-20"},
    {"slug": "kennedy",            "name": "John F. Kennedy",           "number": 35, "term_start": "1961-01-20", "term_end": "1963-11-22"},
    {"slug": "lbjohnson",          "name": "Lyndon B. Johnson",         "number": 36, "term_start": "1963-11-22", "term_end": "1969-01-20"},
    {"slug": "nixon",              "name": "Richard Nixon",             "number": 37, "term_start": "1969-01-20", "term_end": "1974-08-09"},
    {"slug": "ford",               "name": "Gerald Ford",               "number": 38, "term_start": "1974-08-09", "term_end": "1977-01-20"},
    {"slug": "carter",             "name": "Jimmy Carter",              "number": 39, "term_start": "1977-01-20", "term_end": "1981-01-20"},
    {"slug": "reagan",             "name": "Ronald Reagan",             "number": 40, "term_start": "1981-01-20", "term_end": "1989-01-20"},
    {"slug": "bush",               "name": "George H. W. Bush",         "number": 41, "term_start": "1989-01-20", "term_end": "1993-01-20"},
    {"slug": "clinton",            "name": "Bill Clinton",              "number": 42, "term_start": "1993-01-20", "term_end": "2001-01-20"},
    {"slug": "gwbush",             "name": "George W. Bush",            "number": 43, "term_start": "2001-01-20", "term_end": "2009-01-20"},
    {"slug": "barack-obama",       "name": "Barack Obama",              "number": 44, "term_start": "2009-01-20", "term_end": "2017-01-20"},
    {"slug": "trump",              "name": "Donald Trump",              "number": 45, "term_start": "2017-01-20", "term_end": "2021-01-20"},
    {"slug": "biden",              "name": "Joe Biden",                 "number": 46, "term_start": "2021-01-20", "term_end": "2025-01-20"},
]


def fetch_page(slug, max_retries=3):
    """Fetch the Miller Center key events page for a president."""
    url = f"https://millercenter.org/president/{slug}/key-events"
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=30, headers={
                "User-Agent": "PresidentialDashboard/1.0 (academic research)"
            })
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            print(f"  Attempt {attempt+1} failed for {slug}: {e}")
            time.sleep(2 ** attempt)
    return None


def parse_events(html, president_info):
    """Parse Miller Center key-events HTML into structured event dicts."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove nav/footer noise
    main_content = soup.find("main") or soup.find("article") or soup
    for tag in main_content.find_all(["nav", "footer", "header"]):
        tag.decompose()

    text = main_content.get_text(separator="\n")

    date_pattern = re.compile(
        r'^(January|February|March|April|May|June|July|August|'
        r'September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})$',
        re.MULTILINE
    )

    matches = list(date_pattern.finditer(text))
    events = []

    for i, match in enumerate(matches):
        date_str = match.group(0).strip()
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        block = text[start_pos:end_pos].strip()
        lines = [l.strip() for l in block.split("\n") if l.strip()]

        if not lines:
            continue

        title = lines[0]
        description = " ".join(lines[1:]) if len(lines) > 1 else ""

        # Truncate very long descriptions (Miller Center sometimes has embedded essays)
        if len(description) > 1500:
            truncated = description[:1000]
            last_period = truncated.rfind(".")
            if last_period > 500:
                description = truncated[:last_period + 1] + " [truncated]"
            else:
                description = truncated + "... [truncated]"

        # Deduplicate repeated sentences
        sentences = description.split(". ")
        seen = set()
        deduped = []
        for s in sentences:
            s_norm = s.strip().lower()
            if s_norm not in seen and len(s_norm) > 10:
                seen.add(s_norm)
                deduped.append(s.strip())
        description = ". ".join(deduped)

        try:
            parsed_date = datetime.strptime(date_str.replace(",", ""), "%B %d %Y")
            iso_date = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            iso_date = date_str

        source_url = f"https://millercenter.org/president/{president_info['slug']}/key-events"

        events.append({
            "president": president_info["name"],
            "president_number": president_info["number"],
            "term_start": president_info["term_start"],
            "term_end": president_info["term_end"],
            "event_date": iso_date,
            "event_end_date": "",
            "event_title": title,
            "event_description": description,
            "event_category": "",
            "importance": "",
            "impact_score": "",
            "impact_description": "",
            "source_url": source_url,
            "source_name": "Miller Center, University of Virginia",
            "source_secondary": "",
            "is_gap_filler": False,
            "data_source": "miller_center",
        })

    return events


def handle_cleveland(all_events):
    """
    Cleveland served as 22nd and 24th president (non-consecutive).
    Miller Center has one page. Split events by date.
    """
    cleveland_gap_start = datetime.strptime("1889-03-04", "%Y-%m-%d")
    cleveland_gap_end = datetime.strptime("1893-03-04", "%Y-%m-%d")

    for event in all_events:
        if event["president"] == "Grover Cleveland":
            try:
                event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")
                if event_date >= cleveland_gap_end:
                    event["president_number"] = 24
                    event["term_start"] = "1893-03-04"
                    event["term_end"] = "1897-03-04"
                else:
                    event["president_number"] = 22
                    event["term_start"] = "1885-03-04"
                    event["term_end"] = "1889-03-04"
            except ValueError:
                pass
    return all_events


def run_phase1():
    """Scrape all Miller Center key events pages."""
    os.makedirs("data/raw", exist_ok=True)

    all_events = []
    failed = []
    seen_slugs = set()

    for p in PRESIDENTS:
        slug = p["slug"]
        if slug in seen_slugs:
            continue  # Skip duplicate Cleveland entry
        seen_slugs.add(slug)

        print(f"[{p['number']:>2}] {p['name']:<30} ({slug})...", end=" ", flush=True)

        html = fetch_page(slug)
        if html is None:
            print("FAILED")
            failed.append(slug)
            continue

        events = parse_events(html, p)
        print(f"{len(events)} events")
        all_events.extend(events)

        time.sleep(1.0)  # Be polite

    # Handle Cleveland's two terms
    all_events = handle_cleveland(all_events)

    # Sort
    all_events.sort(key=lambda e: (e["president_number"], e["event_date"]))

    # Write CSV
    output_path = "data/raw/miller_center_events.csv"
    if all_events:
        fieldnames = list(all_events[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_events)

    print(f"\n{'='*50}")
    print(f"Total events: {len(all_events)}")
    print(f"Presidents: {len(seen_slugs) - len(failed)}/{len(seen_slugs)}")
    if failed:
        print(f"Failed: {failed}")
    print(f"Output: {output_path}")

    return all_events


if __name__ == "__main__":
    run_phase1()
