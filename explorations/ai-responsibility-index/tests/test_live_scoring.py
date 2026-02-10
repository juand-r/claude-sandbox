"""
Live LLM scoring test -- requires API keys.

Runs a small subset of indicators against a real document to verify:
1. API calls succeed
2. Responses parse correctly
3. Scores are reasonable

Usage:
    # With Anthropic:
    ANTHROPIC_API_KEY=sk-ant-... python tests/test_live_scoring.py

    # With OpenAI:
    OPENAI_API_KEY=sk-... python tests/test_live_scoring.py --model gpt-4o

    # With .env file:
    python tests/test_live_scoring.py
"""

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingest import ingest_pdf
from src.store import VectorStore
from src.indicators import get_indicator_by_id
from src.scorer import Scorer

TEST_DOCS = Path(__file__).parent.parent / "test_docs"

# Test a small subset of indicators to keep costs low
TEST_INDICATORS = ["gov_01", "gov_03", "gov_10"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def run_live_test(pdf_path: str, model: str, provider: str | None = None, api_key: str | None = None):
    """Run live scoring on a few indicators."""
    print(f"\n{'='*60}")
    print(f"LIVE SCORING TEST")
    print(f"Document: {pdf_path}")
    print(f"Model: {model}")
    print(f"{'='*60}\n")

    # Ingest
    print("Ingesting PDF...")
    chunks = ingest_pdf(pdf_path)
    print(f"  {len(chunks)} chunks extracted")

    # Build store
    print("Building vector store...")
    store = VectorStore()
    store.build(chunks)

    # Initialize scorer
    print(f"Initializing scorer (model={model})...")
    scorer = Scorer(model=model, provider=provider, api_key=api_key)
    print(f"  Provider: {scorer.provider}")

    # Score each test indicator
    results = []
    for ind_id in TEST_INDICATORS:
        indicator = get_indicator_by_id(ind_id)
        print(f"\nScoring {ind_id} ({indicator.name})...")

        # Retrieve passages
        retrieval = store.query(indicator.search_terms, top_k=5)
        print(f"  Retrieved {len(retrieval)} passages (best score: {retrieval[0].score:.3f})" if retrieval else "  No passages")

        # Score
        score = scorer.score_indicator(indicator, retrieval)
        results.append(score)

        print(f"  Score: {score.score}/5 {'(DISCLOSED)' if score.disclosed else '(NOT DISCLOSED)'}")
        print(f"  Evidence: {score.evidence[:200]}")
        print(f"  Justification: {score.justification[:200]}")
        print(f"  Pages: {score.source_pages}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    avg = sum(r.score for r in results) / len(results)
    disclosed = sum(1 for r in results if r.disclosed)
    print(f"Average score: {avg:.1f}/5")
    print(f"Disclosed: {disclosed}/{len(results)}")

    for r in results:
        print(f"  {r.indicator_id}: {r.score}/5 {'D' if r.disclosed else '-'} | {r.justification[:80]}")

    # Sanity checks
    print(f"\n{'='*60}")
    print("VALIDATION")
    print(f"{'='*60}")
    all_parsed = all(r.evidence != "PARSE ERROR: Could not parse LLM response." for r in results)
    print(f"  All responses parsed: {'PASS' if all_parsed else 'FAIL'}")

    all_in_range = all(0 <= r.score <= 5 for r in results)
    print(f"  All scores in range 0-5: {'PASS' if all_in_range else 'FAIL'}")

    has_evidence = all(r.evidence for r in results if r.disclosed)
    print(f"  Disclosed items have evidence: {'PASS' if has_evidence else 'FAIL'}")

    if all_parsed and all_in_range:
        print("\n  Live scoring test PASSED.")
    else:
        print("\n  Live scoring test had FAILURES.")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live LLM scoring test")
    parser.add_argument("--pdf", default=str(TEST_DOCS / "csiro_rai_esg.pdf"),
                        help="Path to PDF to score")
    parser.add_argument("--model", "-m", default="claude-sonnet-4-5-20250929",
                        help="Model to use")
    parser.add_argument("--provider", choices=["anthropic", "openai"],
                        help="Force provider")
    parser.add_argument("--api-key", help="API key (or set env var)")
    args = parser.parse_args()

    if not Path(args.pdf).exists():
        print(f"ERROR: PDF not found: {args.pdf}")
        print("Download test documents first. See DATA_SOURCES.md.")
        sys.exit(1)

    run_live_test(args.pdf, args.model, args.provider, args.api_key)
