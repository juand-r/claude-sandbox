# Presidential Actions Dashboard — Data Pipeline

## Project Goal
Build a comprehensive structured dataset of all major actions/events for every US president (1-46), with dates, descriptions, categories, importance scores, and source links. Later: score each event on a -100 to +100 moral impact scale and visualize as a colored heatmap.

## Current State
- Pipeline scripts are written and tested
- Classifier and importance heuristics are tuned
- Demo validated on Theodore Roosevelt (36 events parsed correctly)
- **NEEDS**: Actually running the scraper against millercenter.org (requires network access)

## Architecture

### Data Flow
```
Phase 1: Scrape Miller Center → data/raw/miller_center_events.csv
Phase 2: Enrich (categorize, importance, duration, flags) → data/enriched/events_enriched.csv
Phase 3: Verify integrity → prints report, no file output
```

Wikipedia supplement was planned as Phase 2 originally but is deferred — Miller Center alone gives 15-50 events per president which is sufficient for v1.

### Key Files
- `scrape_miller_center.py` — Fetches and parses all 45 president key-events pages
- `enrich.py` — Categorizes, scores importance (1-5), estimates duration, flags issues  
- `verify.py` — Integrity checks: dates, coverage, categories, flags
- `run_pipeline.py` — Orchestrator: runs all phases in sequence

### Schema (CSV columns)
president, president_number, term_start, term_end, event_date, event_end_date, 
event_title, event_description, event_category, importance, impact_score, 
impact_description, source_url, source_name, source_secondary, is_gap_filler, 
data_source, duration_days_estimate, flags

### Event Categories
DOMESTIC_POLICY, FOREIGN_POLICY, MILITARY, CIVIL_RIGHTS, ECONOMIC, JUDICIAL, 
ENVIRONMENTAL, SCANDAL, ELECTION, EXECUTIVE_ORDER, LEGISLATION, HUMANITARIAN, 
INFRASTRUCTURE, GOVERNANCE, OTHER

### Importance Scale
- 5: Transformative (changed American history)
- 4: Major (significant lasting impact)
- 3: Notable (important at the time)
- 2: Minor (part of the record)
- 1: Routine (placeholder/administrative)

### Intentionally Blank Fields (for later)
- `impact_score`: -100 to +100, filled in scoring phase
- `impact_description`: natural language explanation, filled in scoring phase

## Cleveland Note
Grover Cleveland served as both 22nd and 24th president. Miller Center has one page. 
The scraper handles this by splitting events based on date relative to his two terms.

## Running
```bash
pip install requests beautifulsoup4 pandas
python run_pipeline.py
```

## Known Issues to Watch For
- Some Miller Center pages may have inconsistent HTML structure
- Pre-term events (before inauguration) get flagged but kept
- Same-date events (multiple things on one day) are flagged but kept
- Category classifier is keyword-based; edge cases exist
- Very short presidencies (Harrison: 31 days, Garfield: 199 days) will have few events
