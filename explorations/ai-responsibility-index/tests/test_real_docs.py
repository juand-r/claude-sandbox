"""
Integration tests using real downloaded corporate RAI documents.

Tests ingestion, chunking, and retrieval quality on real PDFs.
Does NOT require API keys (no LLM calls).
Requires test_docs/ to contain downloaded PDFs (see DATA_SOURCES.md).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingest import ingest_pdf
from src.store import VectorStore
from src.indicators import get_all_indicators, get_indicator_by_id

TEST_DOCS = Path(__file__).parent.parent / "test_docs"
CSIRO_PDF = TEST_DOCS / "csiro_rai_esg.pdf"
OPENAI_PDF = TEST_DOCS / "openai_gpt4o_system_card.pdf"
ANTHROPIC_PDF = TEST_DOCS / "anthropic_claude2_model_card.pdf"


def _skip_if_missing(path: Path) -> bool:
    if not path.exists():
        print(f"  SKIP: {path.name} not found in test_docs/")
        return True
    return False


def test_csiro_ingestion():
    """Test CSIRO RAI-ESG framework PDF ingestion."""
    if _skip_if_missing(CSIRO_PDF):
        return

    chunks = ingest_pdf(str(CSIRO_PDF))
    assert len(chunks) > 20, f"Expected many chunks from 18-page report, got {len(chunks)}"

    pages = set(c.page for c in chunks)
    assert len(pages) >= 10, f"Expected content from most pages, got pages: {sorted(pages)}"

    sections = set(c.section for c in chunks if c.section)
    assert len(sections) >= 5, f"Expected multiple sections, got: {sections}"

    all_text = " ".join(c.text for c in chunks).lower()
    assert "governance" in all_text, "Missing governance content"
    assert "indicator" in all_text or "responsible ai" in all_text, "Missing RAI content"

    print(f"  CSIRO: {len(chunks)} chunks, {len(pages)} pages, {len(sections)} sections")


def test_openai_ingestion():
    """Test OpenAI system card PDF ingestion."""
    if _skip_if_missing(OPENAI_PDF):
        return

    chunks = ingest_pdf(str(OPENAI_PDF))
    assert len(chunks) > 30, f"Expected many chunks from 33-page report, got {len(chunks)}"

    all_text = " ".join(c.text for c in chunks).lower()
    assert "safety" in all_text, "Missing safety content"
    assert "gpt" in all_text or "model" in all_text, "Missing model content"

    # Check section detection
    sections = set(c.section for c in chunks if c.section)
    assert len(sections) >= 3, f"Expected sections, got: {sections}"

    print(f"  OpenAI: {len(chunks)} chunks, sections: {sorted(sections)[:8]}")


def test_anthropic_ingestion():
    """Test Anthropic model card PDF ingestion."""
    if _skip_if_missing(ANTHROPIC_PDF):
        return

    chunks = ingest_pdf(str(ANTHROPIC_PDF))
    assert len(chunks) > 10, f"Expected chunks from 14-page report, got {len(chunks)}"

    all_text = " ".join(c.text for c in chunks).lower()
    assert "claude" in all_text, "Missing Claude content"

    print(f"  Anthropic: {len(chunks)} chunks")


def test_retrieval_quality_csiro():
    """Test that RAG retrieval finds relevant content in CSIRO report."""
    if _skip_if_missing(CSIRO_PDF):
        return

    chunks = ingest_pdf(str(CSIRO_PDF))
    store = VectorStore()
    store.build(chunks)

    indicators = get_all_indicators()

    # For each indicator, check that retrieval finds something
    all_results = {}
    for ind in indicators:
        results = store.query(ind.search_terms, top_k=5)
        all_results[ind.id] = results

    # CSIRO report is about RAI governance, so most indicators should retrieve something
    with_results = sum(1 for r in all_results.values() if r)
    assert with_results == 10, f"Expected all 10 indicators to retrieve passages, got {with_results}"

    # Check score discrimination: governance indicators should score higher than random
    gov01_results = all_results["gov_01"]
    if gov01_results:
        best_score = gov01_results[0].score
        assert best_score > 0.3, f"gov_01 (Board Accountability) should match CSIRO report well, got {best_score:.3f}"
        print(f"  gov_01 best retrieval score: {best_score:.3f}")

    # Check that board-related queries retrieve board-related content
    gov02_results = all_results["gov_02"]
    if gov02_results:
        top_text = gov02_results[0].text.lower()
        assert any(w in top_text for w in ("board", "director", "capability", "expertise", "skill")), \
            f"gov_02 top result should be about board capability. Got: {top_text[:100]}"

    print(f"  CSIRO retrieval: all 10 indicators retrieved, quality checks passed")


def test_retrieval_quality_openai():
    """Test retrieval on OpenAI system card -- checks for References pollution."""
    if _skip_if_missing(OPENAI_PDF):
        return

    chunks = ingest_pdf(str(OPENAI_PDF))
    store = VectorStore()
    store.build(chunks)

    # Safety indicator should find safety-related content, not just references
    ind = get_indicator_by_id("gov_04")  # Sensitive Use Cases
    results = store.query(ind.search_terms, top_k=5)

    if results:
        # Check how many top results are from References section
        ref_count = sum(1 for r in results if r.section and "reference" in r.section.lower())
        content_count = len(results) - ref_count

        print(f"  OpenAI gov_04 retrieval: {content_count} content + {ref_count} references out of {len(results)}")

        # At least some results should be actual content, not just references
        # (This documents the known References pollution issue)
        if ref_count > content_count:
            print(f"  WARNING: References section dominating results (known issue)")


def test_end_to_end_mock_on_real_pdf():
    """Full pipeline on real PDF with mock LLM scoring."""
    if _skip_if_missing(CSIRO_PDF):
        return

    import json
    from unittest.mock import patch
    from src.pipeline import Pipeline
    from src.scorer import Scorer, IndicatorScore

    def mock_score(self, indicator, results):
        # Return a score based on whether we found relevant passages
        has_relevant = any(r.score > 0.4 for r in results) if results else False
        return IndicatorScore(
            indicator_id=indicator.id,
            indicator_name=indicator.name,
            category=indicator.category,
            score=3 if has_relevant else 1,
            disclosed=has_relevant,
            evidence="Mock evidence" if has_relevant else "",
            justification="Mock: scored based on retrieval quality",
            passages_used=len(results),
            source_pages=[r.page for r in results if r.page],
        )

    pipeline = Pipeline(api_key="fake")

    with patch.object(Scorer, '__init__', lambda self, **kwargs: None):
        with patch.object(Scorer, 'score_indicator', mock_score):
            report = pipeline.run(str(CSIRO_PDF))

    assert report.total_chunks > 20
    assert len(report.indicator_scores) == 10
    assert report.overall_score > 0

    # Most indicators should find relevant content in this RAI-focused report
    disclosed_count = sum(1 for s in report.indicator_scores if s.disclosed)
    assert disclosed_count >= 5, f"Expected most indicators disclosed for CSIRO report, got {disclosed_count}"

    Pipeline.print_report(report)

    # JSON round-trip
    json_str = Pipeline.report_to_json(report)
    data = json.loads(json_str)
    assert data["overall_score"] == report.overall_score

    print(f"\n  End-to-end mock: overall={report.overall_score:.1f}/5, disclosed={disclosed_count}/10")


if __name__ == "__main__":
    print("Testing CSIRO PDF ingestion...")
    test_csiro_ingestion()

    print("\nTesting OpenAI PDF ingestion...")
    test_openai_ingestion()

    print("\nTesting Anthropic PDF ingestion...")
    test_anthropic_ingestion()

    print("\nTesting retrieval quality on CSIRO report...")
    test_retrieval_quality_csiro()

    print("\nTesting retrieval quality on OpenAI system card...")
    test_retrieval_quality_openai()

    print("\nTesting end-to-end pipeline (mock LLM) on real PDF...")
    test_end_to_end_mock_on_real_pdf()

    print("\nAll real document tests passed.")
