"""
Pipeline Orchestrator

Ties together: ingest → store → retrieve → score → aggregate.

Produces a full RAI Governance report for a company document.
"""

import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path

from .indicators import get_all_indicators, Indicator
from .ingest import ingest, Chunk
from .store import VectorStore, RetrievalResult
from .scorer import Scorer, IndicatorScore

logger = logging.getLogger(__name__)

# CSIRO classification thresholds (adapted from 0-10 binary to 0-5 Likert)
# Original: Strong >= 8/10, Moderate 4-7/10, Weak 0-3/10
# Adapted for 0-5 scale (avg across 10 indicators):
DECISION_THRESHOLDS = {
    "Strong": 4.0,       # avg >= 4.0
    "Moderate": 2.5,     # avg >= 2.5
    "Weak": 1.0,         # avg >= 1.0
    "Unacceptable": 0.0, # avg < 1.0
}

CATEGORY_ORDER = [
    "Board Oversight",
    "RAI Commitment",
    "RAI Implementation",
    "RAI Metrics",
]


@dataclass
class CategoryResult:
    category: str
    indicators: list[IndicatorScore]
    avg_score: float
    disclosure_rate: float  # fraction of indicators where disclosed=True


@dataclass
class AssessmentReport:
    """Full assessment report for a single document."""
    source_file: str
    total_chunks: int
    overall_score: float
    overall_level: str      # Strong / Moderate / Weak / Unacceptable
    disclosure_rate: float  # fraction of indicators with any disclosure
    categories: list[CategoryResult]
    indicator_scores: list[IndicatorScore]


def classify_level(avg_score: float) -> str:
    """Classify an average score into Strong/Moderate/Weak/Unacceptable."""
    if avg_score >= DECISION_THRESHOLDS["Strong"]:
        return "Strong"
    elif avg_score >= DECISION_THRESHOLDS["Moderate"]:
        return "Moderate"
    elif avg_score >= DECISION_THRESHOLDS["Weak"]:
        return "Weak"
    else:
        return "Unacceptable"


class Pipeline:
    """
    Main pipeline for assessing RAI governance from a document.

    Usage:
        pipeline = Pipeline(api_key="sk-...")
        report = pipeline.run("path/to/report.pdf")
        pipeline.print_report(report)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-5-20250929",
        provider: str | None = None,
        embedding_model: str = "all-MiniLM-L6-v2",
        top_k: int = 5,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
    ):
        self.api_key = api_key
        self.model = model
        self.provider = provider
        self.embedding_model = embedding_model
        self.top_k = top_k
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def run(self, filepath: str | Path, indicators: list[Indicator] | None = None) -> AssessmentReport:
        """
        Run the full pipeline on a document.

        Args:
            filepath: Path to PDF or XML file.
            indicators: Optional subset of indicators to score. Defaults to all governance indicators.

        Returns:
            AssessmentReport with all scores and metadata.
        """
        filepath = Path(filepath)
        if indicators is None:
            indicators = get_all_indicators()

        # Step 1: Ingest
        logger.info(f"Ingesting: {filepath}")
        chunks = ingest(filepath, max_chars=self.chunk_size, overlap=self.chunk_overlap)
        logger.info(f"Produced {len(chunks)} chunks")

        if not chunks:
            raise ValueError(f"No text content extracted from {filepath}")

        # Step 2: Build vector store
        logger.info("Building vector store...")
        store = VectorStore(model_name=self.embedding_model)
        store.build(chunks)

        # Step 3: Score each indicator
        scorer = Scorer(model=self.model, provider=self.provider, api_key=self.api_key)
        all_scores: list[IndicatorScore] = []

        for indicator in indicators:
            # Retrieve relevant passages for this indicator
            results = store.query(indicator.search_terms, top_k=self.top_k)
            logger.info(
                f"  {indicator.id}: retrieved {len(results)} passages "
                f"(best score: {results[0].score:.3f})" if results else
                f"  {indicator.id}: no passages retrieved"
            )

            # Score using LLM
            score = scorer.score_indicator(indicator, results)
            all_scores.append(score)
            logger.info(f"  {indicator.id}: score={score.score}/5, disclosed={score.disclosed}")

        # Step 4: Aggregate
        report = self._aggregate(str(filepath), len(chunks), all_scores)
        return report

    def _aggregate(self, source_file: str, total_chunks: int, scores: list[IndicatorScore]) -> AssessmentReport:
        """Aggregate indicator scores into category and overall results."""

        # Group by category
        cat_map: dict[str, list[IndicatorScore]] = {}
        for s in scores:
            cat_map.setdefault(s.category, []).append(s)

        categories = []
        for cat_name in CATEGORY_ORDER:
            cat_scores = cat_map.get(cat_name, [])
            if not cat_scores:
                continue
            avg = sum(s.score for s in cat_scores) / len(cat_scores)
            disc = sum(1 for s in cat_scores if s.disclosed) / len(cat_scores)
            categories.append(CategoryResult(
                category=cat_name,
                indicators=cat_scores,
                avg_score=round(avg, 2),
                disclosure_rate=round(disc, 2),
            ))

        overall_avg = sum(s.score for s in scores) / len(scores) if scores else 0
        overall_disc = sum(1 for s in scores if s.disclosed) / len(scores) if scores else 0

        return AssessmentReport(
            source_file=source_file,
            total_chunks=total_chunks,
            overall_score=round(overall_avg, 2),
            overall_level=classify_level(overall_avg),
            disclosure_rate=round(overall_disc, 2),
            categories=categories,
            indicator_scores=scores,
        )

    @staticmethod
    def print_report(report: AssessmentReport) -> None:
        """Print a human-readable report to stdout."""
        print("=" * 70)
        print("RAI GOVERNANCE ASSESSMENT REPORT")
        print("=" * 70)
        print(f"Source: {report.source_file}")
        print(f"Chunks analyzed: {report.total_chunks}")
        print()
        print(f"OVERALL SCORE: {report.overall_score:.1f} / 5.0  [{report.overall_level}]")
        print(f"Disclosure rate: {report.disclosure_rate:.0%}")
        print()

        for cat in report.categories:
            print(f"--- {cat.category} (avg: {cat.avg_score:.1f}, disclosure: {cat.disclosure_rate:.0%}) ---")
            for ind in cat.indicators:
                status = "DISCLOSED" if ind.disclosed else "NOT DISCLOSED"
                print(f"  [{ind.score}/5] {ind.indicator_name} ({status})")
                if ind.evidence and ind.evidence != "PARSE ERROR: Could not parse LLM response.":
                    # Truncate long evidence for display
                    ev = ind.evidence[:150] + "..." if len(ind.evidence) > 150 else ind.evidence
                    print(f"         Evidence: {ev}")
                print(f"         Justification: {ind.justification[:150]}")
                if ind.source_pages:
                    print(f"         Pages: {ind.source_pages}")
                print()

        print("=" * 70)
        print(f"FINAL ASSESSMENT: {report.overall_level.upper()}")
        print("=" * 70)

    @staticmethod
    def report_to_json(report: AssessmentReport) -> str:
        """Serialize report to JSON."""
        data = {
            "source_file": report.source_file,
            "total_chunks": report.total_chunks,
            "overall_score": report.overall_score,
            "overall_level": report.overall_level,
            "disclosure_rate": report.disclosure_rate,
            "categories": [],
            "indicator_scores": [],
        }
        for cat in report.categories:
            data["categories"].append({
                "category": cat.category,
                "avg_score": cat.avg_score,
                "disclosure_rate": cat.disclosure_rate,
            })
        for s in report.indicator_scores:
            data["indicator_scores"].append({
                "indicator_id": s.indicator_id,
                "indicator_name": s.indicator_name,
                "category": s.category,
                "score": s.score,
                "disclosed": s.disclosed,
                "evidence": s.evidence,
                "justification": s.justification,
                "passages_used": s.passages_used,
                "source_pages": s.source_pages,
            })
        return json.dumps(data, indent=2)
