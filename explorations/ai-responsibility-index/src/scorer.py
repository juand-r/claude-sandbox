"""
LLM Scoring Module

Scores each indicator by sending retrieved passages + indicator metadata
to an LLM, which returns a structured score with evidence and justification.

Supports Anthropic Claude API. Could be extended to OpenAI.
"""

import json
import logging
import os
import re
from dataclasses import dataclass

try:
    import anthropic
except ImportError:
    anthropic = None

from .indicators import Indicator, RUBRIC_PREAMBLE
from .store import RetrievalResult

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
MAX_PASSAGE_CHARS = 8000  # limit total passage text sent to LLM


@dataclass
class IndicatorScore:
    """Result of scoring one indicator against a document."""
    indicator_id: str
    indicator_name: str
    category: str
    score: int              # 0-5
    disclosed: bool         # whether the company disclosed anything relevant
    evidence: str           # direct quotes or references from the document
    justification: str      # why this score was assigned
    passages_used: int      # how many retrieved passages were sent to the LLM
    source_pages: list[int | None]  # page numbers of passages used


class Scorer:
    """
    Scores indicators using an LLM.

    Usage:
        scorer = Scorer()
        result = scorer.score_indicator(indicator, retrieval_results)
    """

    def __init__(self, model: str = DEFAULT_MODEL, api_key: str | None = None):
        if anthropic is None:
            raise ImportError("anthropic is required. Install with: pip install anthropic")

        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def score_indicator(self, indicator: Indicator, results: list[RetrievalResult]) -> IndicatorScore:
        """
        Score a single indicator using retrieved passages.

        Args:
            indicator: The indicator to score.
            results: Retrieved passages from the vector store.

        Returns:
            IndicatorScore with score, evidence, and justification.
        """
        # Format passages with citations
        passages_text = self._format_passages(results)
        source_pages = [r.page for r in results if r.page is not None]

        # Build the rubric text
        rubric_text = RUBRIC_PREAMBLE + "\n\nSpecific rubric for this indicator:\n"
        for level, desc in sorted(indicator.rubric.items()):
            rubric_text += f"  {level} = {desc}\n"

        # Fill in the prompt template
        prompt = indicator.prompt_template.format(
            rubric=rubric_text,
            passages=passages_text,
        )

        # Add expert knowledge as system context
        system_msg = (
            "You are an expert ESG analyst specializing in Responsible AI assessment. "
            "You are evaluating corporate disclosures for evidence of responsible AI practices.\n\n"
            f"Domain knowledge for this indicator:\n{indicator.knowledge}\n\n"
            "Be rigorous and skeptical. Score based on concrete evidence, not aspirational language. "
            "If the passages contain no relevant information, score 0 and set disclosed to false."
        )

        logger.info(f"Scoring indicator: {indicator.id} ({indicator.name})")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_msg,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the JSON response
        raw = response.content[0].text
        parsed = self._parse_response(raw, indicator)

        return IndicatorScore(
            indicator_id=indicator.id,
            indicator_name=indicator.name,
            category=indicator.category,
            score=parsed["score"],
            disclosed=parsed["disclosed"],
            evidence=parsed["evidence"],
            justification=parsed["justification"],
            passages_used=len(results),
            source_pages=source_pages,
        )

    def _format_passages(self, results: list[RetrievalResult]) -> str:
        """Format retrieved passages with source citations, respecting char limit."""
        if not results:
            return "[No relevant passages found in the document.]"

        parts = []
        total_chars = 0

        for i, r in enumerate(results):
            citation = f"[Source: {r.source_file}"
            if r.page:
                citation += f", page {r.page}"
            if r.section:
                citation += f", section: {r.section}"
            citation += f", relevance: {r.score:.3f}]"

            entry = f"--- Passage {i+1} {citation} ---\n{r.text}\n"

            if total_chars + len(entry) > MAX_PASSAGE_CHARS:
                break
            parts.append(entry)
            total_chars += len(entry)

        return "\n".join(parts)

    def _parse_response(self, raw: str, indicator: Indicator) -> dict:
        """
        Parse the LLM's JSON response. Handles common failure modes:
        - Response wrapped in markdown code blocks
        - Response with extra text before/after JSON
        - Malformed JSON
        """
        # Try to extract JSON from the response
        # First: look for ```json ... ``` blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw, re.DOTALL)
        if json_match:
            raw = json_match.group(1)
        else:
            # Try to find a bare JSON object
            json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', raw, re.DOTALL)
            if json_match:
                raw = json_match.group(0)

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse LLM response for {indicator.id}. Raw: {raw[:200]}")
            return {
                "score": 0,
                "disclosed": False,
                "evidence": "PARSE ERROR: Could not parse LLM response.",
                "justification": f"Raw response: {raw[:500]}",
            }

        # Validate and clamp score
        score = parsed.get("score", 0)
        if not isinstance(score, int):
            try:
                score = int(score)
            except (ValueError, TypeError):
                score = 0
        score = max(0, min(5, score))

        return {
            "score": score,
            "disclosed": bool(parsed.get("disclosed", False)),
            "evidence": str(parsed.get("evidence", "")),
            "justification": str(parsed.get("justification", "")),
        }
