"""
Test PDF ingestion with programmatically generated PDFs.

Creates realistic multi-page PDF documents with:
- Section headings (larger font)
- Body text paragraphs
- Multiple pages
- Tables (text-based)
- Edge cases: empty pages, very long paragraphs, headers/footers
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import fitz  # PyMuPDF for creating test PDFs
from src.ingest import ingest_pdf, ingest, Chunk


def create_test_pdf(filepath: str, pages: list[list[tuple[str, float]]]) -> None:
    """
    Create a test PDF with specified text content.

    Args:
        filepath: Where to save the PDF.
        pages: List of pages, each page is a list of (text, font_size) tuples.
               If text overflows a page, it continues on a new page.
    """
    doc = fitz.open()
    for page_content in pages:
        page = doc.new_page(width=595, height=842)  # A4
        y = 50
        for text, font_size in page_content:
            lines = text.split('\n')
            for line in lines:
                if y > 790:
                    # Overflow: create a new page and continue
                    page = doc.new_page(width=595, height=842)
                    y = 50
                page.insert_text(
                    (50, y),
                    line,
                    fontsize=font_size,
                    fontname="helv",
                )
                y += font_size * 1.4
            y += 10
    doc.save(filepath)
    doc.close()


def test_basic_pdf():
    """Test basic PDF with headings and body text."""
    pages = [
        [
            ("Corporate Governance Report 2024", 18),
            ("Board Oversight of AI", 16),
            ("The Board of Directors has established an AI Ethics Committee\n"
             "under the Risk Committee. The committee meets quarterly to\n"
             "review all artificial intelligence deployments and associated\n"
             "risks across the organization. Board members receive structured\n"
             "AI risk reports at each quarterly meeting.", 11),
            ("Responsible AI Policy", 16),
            ("We published our Responsible AI Framework in March 2024,\n"
             "available on our corporate website. The framework is aligned\n"
             "with the EU AI Act and ISO/IEC 42001. It covers fairness,\n"
             "transparency, accountability, safety, and privacy.", 11),
        ],
        [
            ("AI Workforce Development", 16),
            ("All employees involved in AI development must complete our\n"
             "mandatory Responsible AI certification program annually.\n"
             "In 2024, 98% of eligible employees completed the certification.\n"
             "The curriculum covers bias detection, fairness testing,\n"
             "privacy engineering, and incident reporting procedures.", 11),
            ("AI Metrics and Performance", 16),
            ("We report the following RAI metrics quarterly:\n"
             "Bias audit completion rate: 97%\n"
             "Fairness score: 0.92 average\n"
             "AI energy consumption: 14,200 MWh\n"
             "AI incident rate: 1.8 per 100 deployments", 11),
        ],
    ]

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        filepath = f.name

    create_test_pdf(filepath, pages)
    chunks = ingest_pdf(filepath)

    assert len(chunks) > 0, "No chunks extracted from PDF"

    all_text = " ".join(c.text for c in chunks)
    assert "AI Ethics Committee" in all_text, "Missing governance text"
    assert "Responsible AI Framework" in all_text, "Missing policy text"
    assert "certification" in all_text, "Missing training text"
    assert "Bias audit" in all_text or "bias audit" in all_text, "Missing metrics text"

    # Check page numbers are assigned
    pages_found = set(c.page for c in chunks)
    assert 1 in pages_found, "Page 1 not found"
    assert 2 in pages_found, "Page 2 not found"

    # Check section detection (headings have font_size > 13)
    sections = set(c.section for c in chunks if c.section)
    assert len(sections) > 0, f"No sections detected. Chunks: {[(c.section, c.text[:50]) for c in chunks]}"

    print(f"  Basic PDF: {len(chunks)} chunks, pages: {sorted(pages_found)}, sections: {sections}")
    for c in chunks[:4]:
        preview = c.text[:70].replace('\n', ' ')
        print(f"    p{c.page} [{c.section}] {preview}...")


def test_empty_pages():
    """PDF with some empty pages should not crash."""
    pages = [
        [("Title Page", 18)],
        [],  # empty page
        [("Content on page 3 with enough text to make a chunk.\n"
          "The board has oversight of AI through its technology committee.\n"
          "This committee reviews all AI deployments quarterly.", 11)],
        [],  # another empty page
    ]

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        filepath = f.name

    create_test_pdf(filepath, pages)
    chunks = ingest_pdf(filepath)

    # Should get chunks from pages 1 and 3, skip empty pages
    pages_with_content = set(c.page for c in chunks)
    assert 2 not in pages_with_content, "Empty page 2 should produce no chunks"
    print(f"  Empty pages: {len(chunks)} chunks from pages {sorted(pages_with_content)}")


def test_long_paragraphs():
    """Test chunking of very long text that exceeds chunk size."""
    # Build long text as separate lines (PDF renderer splits on \n)
    sentence = "The company approach to responsible AI governance encompasses multiple dimensions of oversight."
    lines = [sentence for _ in range(30)]  # ~30 lines, well over 500 chars total
    long_text = "\n".join(lines)

    pages = [
        [
            ("Detailed Governance Discussion", 16),
            (long_text, 11),
        ],
    ]

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        filepath = f.name

    create_test_pdf(filepath, pages)
    chunks = ingest_pdf(filepath, max_chars=500)

    total_chars = sum(len(c.text) for c in chunks)
    assert len(chunks) > 1, f"Long text ({total_chars} chars) should be split, got {len(chunks)} chunks"
    print(f"  Long paragraphs: {len(chunks)} chunks, total {total_chars} chars")
    for i, c in enumerate(chunks):
        print(f"    chunk {i}: {len(c.text)} chars, page {c.page}")


def test_auto_detect():
    """Test that ingest() auto-detects PDF files."""
    pages = [
        [("Test document for auto-detection.", 11)],
    ]

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        filepath = f.name

    create_test_pdf(filepath, pages)
    chunks = ingest(filepath)

    assert len(chunks) > 0, "Auto-detect should handle .pdf"
    print(f"  Auto-detect .pdf: OK ({len(chunks)} chunks)")


def test_section_heading_detection():
    """Test that section headings are detected from font size."""
    pages = [
        [
            ("Annual Report", 20),               # title, should be detected
            ("Section 1: Governance", 16),        # heading, should be detected
            ("Some body text about governance practices and procedures.", 10),
            ("Section 2: Risk Management", 16),   # heading, should be detected
            ("More body text about risk management frameworks.", 10),
            ("2.1 AI-Specific Risks", 14),        # sub-heading, should be detected
            ("Details about AI risk assessment and mitigation.", 10),
        ],
    ]

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        filepath = f.name

    create_test_pdf(filepath, pages)
    chunks = ingest_pdf(filepath)

    sections = [c.section for c in chunks]
    # At least some sections should be detected (font size > 13)
    non_none_sections = [s for s in sections if s is not None]
    assert len(non_none_sections) > 0, f"No sections detected. All chunks: {[(c.section, c.text[:40]) for c in chunks]}"

    print(f"  Section detection: {len(non_none_sections)} chunks have sections")
    for c in chunks:
        preview = c.text[:60].replace('\n', ' ')
        print(f"    [{c.section}] {preview}...")


def test_multipage_section_continuity():
    """Test that section name carries over across pages."""
    pages = [
        [
            ("AI Governance", 16),
            ("First page content about AI governance and board oversight.\n"
             "The committee meets quarterly.", 11),
        ],
        [
            # No heading on page 2 -- section should carry from page 1
            ("Continued discussion of governance practices.\n"
             "The board receives structured reports.", 11),
        ],
        [
            ("New Section: Implementation", 16),
            ("Content under the new section about implementation details.", 11),
        ],
    ]

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        filepath = f.name

    create_test_pdf(filepath, pages)
    chunks = ingest_pdf(filepath)

    # Page 2 chunks should inherit "AI Governance" section from page 1
    page2_chunks = [c for c in chunks if c.page == 2]
    if page2_chunks:
        assert page2_chunks[0].section == "AI Governance", \
            f"Page 2 should inherit section from page 1, got: {page2_chunks[0].section}"
        print("  Section continuity across pages: OK")

    # Page 3 should have the new section
    page3_chunks = [c for c in chunks if c.page == 3]
    if page3_chunks:
        assert page3_chunks[0].section == "New Section: Implementation", \
            f"Page 3 should have new section, got: {page3_chunks[0].section}"
        print("  New section on page 3: OK")

    print(f"  Multipage sections: {len(chunks)} chunks total")


if __name__ == "__main__":
    print("Testing basic PDF ingestion...")
    test_basic_pdf()

    print("\nTesting empty pages...")
    test_empty_pages()

    print("\nTesting long paragraphs / chunking...")
    test_long_paragraphs()

    print("\nTesting auto-detection...")
    test_auto_detect()

    print("\nTesting section heading detection...")
    test_section_heading_detection()

    print("\nTesting multipage section continuity...")
    test_multipage_section_continuity()

    print("\nAll PDF tests passed.")
