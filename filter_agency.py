#!/usr/bin/env python3
"""
Filter presidential events to only those where the president had direct agency.

Approach: Match president's name + action verb anywhere in the description.
Miller Center descriptions explicitly state who did what, so if the president
is described as acting, they had agency. If only Congress/Court/states/others
are acting, they didn't.
"""

import csv
import re

INPUT_ENRICHED = 'data/enriched/events_enriched.csv'
INPUT_SCORED = 'data/scored/events_scored.csv'
OUTPUT_ENRICHED = 'data/enriched/events_agency_filtered.csv'
OUTPUT_SCORED = 'data/scored/events_scored_filtered.csv'

# Action verbs that indicate presidential agency when preceded by president's name
ACTION_VERBS = (
    r'(signs?|vetoes?|issues?|orders?|appoints?|nominat\w*|directs?|sends?|'
    r'deploys?|announc\w*|delivers?|declar\w*|authoriz\w*|approv\w*|propos\w*|'
    r'instruct\w*|dismiss\w*|fires?|removes?|pardons?|commut\w*|grants?|'
    r'suspends?|revers\w*|withdraws?|recalls?|recogniz\w*|refus\w*|rejects?|'
    r'accepts?|negotiat\w*|launch\w*|invad\w*|attacks?|bombs?|interven\w*|'
    r'dispatch\w*|mobiliz\w*|address\w*|calls?|convenes?|submits?|'
    r'recommend\w*|endors\w*|champions?|push\w*|pledg\w*|agrees?|extends?|'
    r'impos\w*|enforc\w*|implement\w*|execut\w*|begins?|initiat\w*|'
    r'opens?|halts?|stops?|bans?|prohibits?|blocks?|freez\w*|seiz\w*|'
    r'nationaliz\w*|reorganiz\w*|reforms?|expands?|reduc\w*|cuts?|rais\w*|'
    r'eliminat\w*|asks?|urg\w*|demands?|warns?|threatens?|invit\w*|meets?|'
    r'welcomes?|receiv\w*|hosts?|travels?|visits?|tours?|purchas\w*|'
    r'acquir\w*|annex\w*|selects?|chooses?|picks?|commissions?|assigns?|'
    r'transfers?|creates?|establish\w*|founds?|forms?|overrul\w*|rescinds?|'
    r'revok\w*|cancels?|reaffirms?|asserts?|invok\w*|unveils?|introduc\w*|'
    r'presents?|releas\w*|publish\w*|articulat\w*|outlin\w*|requests?|'
    r'seeks?|petitions?|rallies|campaigns?|runs?|concedes?|offers?|'
    r'brokers?|mediat\w*|arbitrat\w*|facilitat\w*|arrang\w*|names?|'
    r'makes?|challeng\w*|plans?|lifts?|supports?|opposes?|maintains?|'
    r'continues?|decides?|takes?|moves?|assumes?|swears?|sworn|'
    r'responds?|replac\w*|pursu\w*|desegregat\w*|integrat\w*|'
    r'proclaims?|maneuver\w*|pressur\w*|persuad\w*|convinc\w*|'
    r'oversees?|manages?|commands?|leads?|head\w*|spearhead\w*|'
    r'championed|backed|embraced|promoted|favored|endorsed|championed|'
    r'fought|battled|resisted|defied|confronted|challenged|demanded|'
    r'asserts?|affirms?|insists?|contends?|maintains?|argues?|'
    r'vows?|promises?|commits?|guarantees?|ensures?|secures?)'
)


def has_presidential_agency(row):
    """Determine if the president had direct agency in this event."""
    title = row['event_title'].strip()
    title_lower = title.lower()
    desc = row['event_description'].strip()
    pres_full = row['president']
    pres = pres_full.split()[-1]  # Last name
    number = int(row['president_number'])
    category = row['event_category']

    # Build list of name variants for this president
    name_variants = [pres, f'President {pres}']
    # Handle common abbreviations/nicknames
    NICKNAMES = {
        'Franklin D. Roosevelt': ['FDR'],
        'Dwight D. Eisenhower': ['Ike', 'Eisenhower'],
        'John F. Kennedy': ['JFK'],
        'Lyndon B. Johnson': ['LBJ'],
    }
    aliases = NICKNAMES.get(pres_full, [])
    name_variants.extend(aliases)
    # Create regex alternation for all name variants
    names_re = '|'.join(re.escape(n) for n in name_variants)

    # ── Always keep inaugurations ──
    if 'inaugurat' in title_lower:
        return True, 'inauguration'

    # ── Always remove statehood ──
    if re.search(r'(becomes? a state|admitted to the union|statehood|joins the union|joins union)', title_lower):
        return False, 'statehood'
    if re.search(r'(becomes? a state|admitted .* state|joins the union)', desc.lower()):
        if not re.search(rf'(President|{pres})', desc):
            return False, 'statehood_desc'

    # ── President + action verb anywhere in description ──
    # Match any name variant + action verb
    if re.search(rf'(?:{names_re})\s+{ACTION_VERBS}', desc, re.IGNORECASE):
        return True, 'president_action'
    # "the president [verb]"
    if re.search(rf'the\s+president\s+{ACTION_VERBS}', desc, re.IGNORECASE):
        return True, 'the_president_action'

    # ── Possessive presidential agency ──
    # "[Name]'s [action noun]"
    if re.search(rf"(?:{names_re})'?s?\s+(attempt|decision|order|directive|request|direction|instruction|behest|initiative|guidance|leadership|message|address|plan|proposal|policy|agenda|veto|proclamation|decree|executive order|action|intervention|campaign|strategy|vision|program|effort|push|drive)", desc, re.IGNORECASE):
        return True, 'president_possessive'

    # "at/under/by [Name]'s direction/order/request"
    if re.search(rf"(at|under|by|with|on)\s+(?:{names_re})'?s?\s+(support|approval|backing|direction|order|request|instruction|urging|insistence|recommendation|initiative|behest|guidance|leadership|command)", desc, re.IGNORECASE):
        return True, 'president_direction'

    # ── Presidential elections (about this president winning/losing) ──
    if re.search(rf'(?:{names_re})\s+(is\s+)?(elected|reelected|re-elected|wins|loses|lost|defeated|concedes)', desc, re.IGNORECASE):
        return True, 'election_result'
    if re.search(r'(reelect|re-elect)', title_lower) and not re.search(r'does not|declines|refuses', title_lower):
        return True, 'reelection_title'

    # ── Executive orders (always presidential) ──
    if category == 'EXECUTIVE_ORDER':
        return True, 'executive_order'

    # ── Appointment in title ──
    if re.search(r'^(appoint|nominat)', title_lower):
        return True, 'appointment_title'

    # ── Farewell address ──
    if 'farewell' in title_lower:
        return True, 'farewell'

    # ── President shot/assassinated/dies in office/impeached ──
    if re.search(rf'(?:{names_re})\s+(is\s+|was\s+)?(shot|assassinat|dies|died|dead|impeach|wounded|killed|passed away)', desc, re.IGNORECASE):
        return True, 'president_personal'
    if re.search(rf'(shot|shoots|assassinat|kill)\w*\s+(President\s+)?\w*\s*(?:{names_re})', desc, re.IGNORECASE):
        return True, 'president_personal'
    if re.search(rf'President\s+\w+\s+\w+\s+(?:{names_re})\s+was\s+(shot|killed|assassinat|wounded)', desc, re.IGNORECASE):
        return True, 'president_personal'

    # ── President "sworn in" ──
    if re.search(rf'(?:{names_re})\s+(is\s+)?(sworn\s+in|takes\s+(the\s+)?(presidential\s+)?oath)', desc, re.IGNORECASE):
        return True, 'sworn_in'

    # ── State of the Union / annual message / fireside chat ──
    if re.search(r'(state of the union|annual message|message to congress|fireside chat)', title_lower):
        if re.search(rf'(?:{names_re}|President)', desc, re.IGNORECASE):
            return True, 'address_to_congress'

    # ── "[Name] declares/says" in title ──
    if re.search(rf'(?:{names_re})\s+{ACTION_VERBS}', title, re.IGNORECASE):
        return True, 'title_action'

    # ── Default: no clear presidential agency ──
    return False, 'no_clear_agency'


def filter_csv(input_path, output_path):
    """Filter a CSV, keeping only events with presidential agency."""
    with open(input_path) as f:
        rows = list(csv.DictReader(f))

    kept = []
    removed = []
    reasons = {}

    for row in rows:
        keep, reason = has_presidential_agency(row)
        reasons[reason] = reasons.get(reason, 0) + 1
        if keep:
            kept.append(row)
        else:
            removed.append(row)

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(kept)

    return rows, kept, removed, reasons


def main():
    # Filter enriched CSV
    rows, kept, removed, reasons = filter_csv(INPUT_ENRICHED, OUTPUT_ENRICHED)

    # Filter scored CSV (same logic, different input/output)
    import os
    if os.path.exists(INPUT_SCORED):
        filter_csv(INPUT_SCORED, OUTPUT_SCORED)
        print(f'Also wrote: {OUTPUT_SCORED}')

    # Print summary
    print(f'Total events: {len(rows)}')
    print(f'Kept (presidential agency): {len(kept)}')
    print(f'Removed (no direct agency): {len(removed)}')
    print(f'\nClassification reasons:')
    for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f'  {reason}: {count}')

    # Per-president counts
    print(f'\nPer-president:')
    pres_counts = {}
    for row in rows:
        p = f'{row["president"]} (#{row["president_number"]})'
        keep, _ = has_presidential_agency(row)
        if p not in pres_counts:
            pres_counts[p] = [0, 0]
        pres_counts[p][0] += 1
        if keep:
            pres_counts[p][1] += 1
    for p, (total, kept_n) in pres_counts.items():
        pct = round(100 * kept_n / total) if total else 0
        print(f'  {p}: {kept_n}/{total} ({pct}%)')


if __name__ == '__main__':
    main()
