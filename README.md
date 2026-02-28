# Presidential Actions Dashboard — Data Pipeline

Structured dataset of major actions/events for all 46 US presidents.

## Quick Start

```bash
pip install -r requirements.txt
python run_pipeline.py
```

This runs three phases:
1. **Scrape** — Fetches Miller Center key-events pages for all 45 presidents (~2 min)
2. **Enrich** — Categorizes, scores importance, estimates duration, flags issues
3. **Verify** — Integrity checks and summary report

## Output

`data/enriched/events_enriched.csv` with columns:

| Column | Description |
|--------|-------------|
| president | Full name |
| president_number | 1-46 |
| term_start / term_end | ISO dates |
| event_date | Date of event |
| event_end_date | Estimated end date |
| event_title | Short title |
| event_description | 1-3 sentence description |
| event_category | One of 15 categories |
| importance | 1-5 scale |
| impact_score | -100 to +100 (**blank — for later**) |
| impact_description | Natural language (**blank — for later**) |
| source_url | Link to Miller Center page |
| flags | PRE_TERM, SAME_DATE_x2, etc. |

## What's Next

1. **Scoring phase**: Fill `impact_score` and `impact_description` for each event
2. **Visualization**: Colored rectangle heatmap — presidents on x-axis, events stacked vertically, red (-100) to green (+100)
