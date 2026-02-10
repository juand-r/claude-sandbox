"""
LLM Scoring Module

Scores each indicator by sending retrieved passages + indicator metadata
to an LLM, which returns a structured score with evidence and justification.

Supports both Anthropic (Claude) and OpenAI (GPT) APIs.
Provider is selected by the model name prefix or explicit provider argument.
"""

import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load .env from project root or working directory
    for env_path in [
        Path(__file__).parent.parent / ".env",
        Path.cwd() / ".env",
    ]:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

from .indicators import Indicator, RUBRIC_PREAMBLE
from .store import RetrievalResult

logger = logging.getLogger(__name__)

MAX_PASSAGE_CHARS = 8000  # limit total passage text sent to LLM

# Model defaults per provider
ANTHROPIC_DEFAULT = "claude-sonnet-4-5-20250929"
OPENAI_DEFAULT = "gpt-4o"


def _detect_provider(model: str) -> str:
    """Detect provider from model name."""
    model_lower = model.lower()
    if any(p in model_lower for p in ("claude", "sonnet", "haiku", "opus")):
        return "anthropic"
    if any(p in model_lower for p in ("gpt", "o1", "o3")):
        return "openai"
    raise ValueError(
        f"Cannot detect provider for model '{model}'. "
        f"Use a model name containing 'claude'/'sonnet'/'haiku'/'opus' for Anthropic, "
        f"or 'gpt'/'o1'/'o3' for OpenAI."
    )


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
    Scores indicators using an LLM (Anthropic or OpenAI).

    Provider is auto-detected from model name, or can be set explicitly.

    Usage:
        scorer = Scorer(model="claude-sonnet-4-5-20250929")   # uses Anthropic
        scorer = Scorer(model="gpt-4o")                       # uses OpenAI
        scorer = Scorer(model="gpt-4o", provider="openai")    # explicit
    """

    def __init__(
        self,
        model: str = ANTHROPIC_DEFAULT,
        provider: str | None = None,
        api_key: str | None = None,
    ):
        self.model = model
        self.provider = provider or _detect_provider(model)

        if self.provider == "anthropic":
            if anthropic is None:
                raise ImportError("anthropic is required. Install: pip install anthropic")
            key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError(
                    "No Anthropic API key found. Set ANTHROPIC_API_KEY env var or pass api_key."
                )
            self.client = anthropic.Anthropic(api_key=key)

        elif self.provider == "openai":
            if openai is None:
                raise ImportError("openai is required. Install: pip install openai")
            key = api_key or os.environ.get("OPENAI_API_KEY")
            if not key:
                raise ValueError(
                    "No OpenAI API key found. Set OPENAI_API_KEY env var or pass api_key."
                )
            self.client = openai.OpenAI(api_key=key)

        else:
            raise ValueError(f"Unknown provider: {self.provider}. Use 'anthropic' or 'openai'.")

        logger.info(f"Scorer initialized: provider={self.provider}, model={self.model}")

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

        # System message with expert knowledge
        system_msg = (
            "You are an expert ESG analyst specializing in Responsible AI assessment. "
            "You are evaluating corporate disclosures for evidence of responsible AI practices.\n\n"
            f"Domain knowledge for this indicator:\n{indicator.knowledge}\n\n"
            "Be rigorous and skeptical. Score based on concrete evidence, not aspirational language. "
            "If the passages contain no relevant information, score 0 and set disclosed to false."
        )

        logger.info(f"Scoring indicator: {indicator.id} ({indicator.name})")

        # Call the appropriate API
        if self.provider == "anthropic":
            raw = self._call_anthropic(system_msg, prompt)
        else:
            raw = self._call_openai(system_msg, prompt)

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

    def _call_anthropic(self, system_msg: str, prompt: str) -> str:
        """Call Anthropic Claude API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_msg,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _call_openai(self, system_msg: str, prompt: str) -> str:
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

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
