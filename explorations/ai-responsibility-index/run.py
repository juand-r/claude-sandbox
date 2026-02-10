#!/usr/bin/env python3
"""
AI Responsibility Index - CLI Entry Point

Score a corporate report on RAI governance indicators.

Usage:
    python run.py <path-to-pdf-or-xml> [options]

Examples:
    python run.py report.pdf
    python run.py report.pdf --model gpt-4o
    python run.py report.pdf --output results.json --top-k 8
    python run.py report.xml --model claude-sonnet-4-5-20250929 -v
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent to path so we can import src
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(
        description="AI Responsibility Index: Score corporate reports on RAI governance.",
    )
    parser.add_argument(
        "filepath",
        help="Path to a PDF or XML corporate report",
    )
    parser.add_argument(
        "--output", "-o",
        help="Write JSON results to this file (in addition to printing)",
    )
    parser.add_argument(
        "--model", "-m",
        default="claude-sonnet-4-5-20250929",
        help="LLM model for scoring. Claude models use Anthropic, GPT models use OpenAI. "
             "(default: claude-sonnet-4-5-20250929)",
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        help="Force a specific API provider (default: auto-detect from model name)",
    )
    parser.add_argument(
        "--embedding-model",
        default="all-MiniLM-L6-v2",
        help="Sentence-transformers model for embeddings (default: all-MiniLM-L6-v2)",
    )
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=5,
        help="Number of passages to retrieve per indicator (default: 5)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1500,
        help="Target chunk size in characters (default: 1500)",
    )
    parser.add_argument(
        "--api-key",
        help="API key (default: uses ANTHROPIC_API_KEY or OPENAI_API_KEY env var, or .env file)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Validate input file
    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if filepath.suffix.lower() not in ('.pdf', '.xml', '.xbrl', '.html', '.xhtml'):
        print(f"Error: Unsupported file type: {filepath.suffix}", file=sys.stderr)
        print("Supported: .pdf, .xml, .xbrl", file=sys.stderr)
        sys.exit(1)

    # Run pipeline
    pipeline = Pipeline(
        api_key=args.api_key,
        model=args.model,
        provider=args.provider,
        embedding_model=args.embedding_model,
        top_k=args.top_k,
        chunk_size=args.chunk_size,
    )

    try:
        report = pipeline.run(filepath)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Output results
    Pipeline.print_report(report)

    if args.output:
        json_str = Pipeline.report_to_json(report)
        output_path = Path(args.output)
        output_path.write_text(json_str)
        print(f"\nJSON results written to: {output_path}")


if __name__ == "__main__":
    main()
