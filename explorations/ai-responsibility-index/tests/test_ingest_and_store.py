"""
Test ingestion and vector store components (no API key needed).
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingest import chunk_text, ingest_xml, Chunk
from src.store import VectorStore


def test_chunk_text():
    """Test text chunking with paragraph boundaries."""
    text = "Paragraph one about AI governance.\n\nParagraph two about board oversight.\n\n" + \
           "Paragraph three about responsible AI policy and framework alignment with standards."

    chunks = chunk_text(text, max_chars=100, overlap=20)
    assert len(chunks) >= 2, f"Expected >= 2 chunks, got {len(chunks)}"
    # Verify all text is represented
    combined = " ".join(chunks)
    assert "AI governance" in combined
    assert "board oversight" in combined
    assert "responsible AI policy" in combined
    print(f"  chunk_text: {len(text)} chars -> {len(chunks)} chunks OK")


def test_chunk_text_short():
    """Short text should not be split."""
    text = "This is a short text."
    chunks = chunk_text(text, max_chars=1000)
    assert len(chunks) == 1
    assert chunks[0] == text
    print("  chunk_text short: OK")


def test_xml_ingestion():
    """Test XML ingestion with a synthetic ESG report."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<report>
    <governance>
        <section title="Board Oversight">
            Our Board of Directors has established an AI Ethics Committee
            that meets quarterly to review all artificial intelligence deployments.
            The committee is chaired by Dr. Jane Smith, who has 20 years of
            experience in machine learning and AI systems. The board receives
            structured AI risk reports at least annually, with ad-hoc updates
            for significant incidents.
        </section>
        <section title="AI Policy">
            We published our Responsible AI Policy in 2023, aligned with the
            EU AI Act and ISO/IEC 42001. The policy covers fairness, transparency,
            accountability, and safety. All high-risk AI applications require
            a dedicated review by our AI Ethics Board before deployment.
        </section>
    </governance>
    <social>
        <section title="Employee Training">
            100% of our AI engineering team completed our mandatory Responsible
            AI certification program in 2023. The program covers bias detection,
            fairness testing, privacy-preserving techniques, and incident
            reporting procedures. We also conducted board-level AI literacy
            workshops for all directors.
        </section>
    </social>
    <metrics>
        <section title="AI Metrics">
            In 2023, we conducted bias audits on 95% of our customer-facing
            AI models. We reduced AI-related incidents by 30% year-over-year.
            Our AI systems consumed 12,500 MWh of energy, a 15% reduction
            from 2022 through model optimization. We track and report these
            metrics quarterly.
        </section>
    </metrics>
</report>"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(xml_content)
        f.flush()
        chunks = ingest_xml(f.name)

    assert len(chunks) > 0, "No chunks extracted from XML"
    # Check that content was extracted
    all_text = " ".join(c.text for c in chunks)
    assert "AI Ethics Committee" in all_text
    assert "Responsible AI Policy" in all_text
    assert "bias audits" in all_text
    print(f"  XML ingestion: {len(chunks)} chunks OK")
    return chunks


def test_vector_store(chunks: list[Chunk]):
    """Test vector store build and query."""
    store = VectorStore()
    store.build(chunks)
    assert store.index.ntotal == len(chunks)

    # Query for board oversight
    results = store.query(["board AI oversight", "AI governance board"], top_k=3)
    assert len(results) > 0
    assert any("board" in r.text.lower() or "committee" in r.text.lower() for r in results)
    print(f"  Vector store query (board oversight): top result score={results[0].score:.3f} OK")

    # Query for AI metrics
    results = store.query(["AI performance metrics", "bias audit results"], top_k=3)
    assert len(results) > 0
    assert any("bias" in r.text.lower() or "metric" in r.text.lower() for r in results)
    print(f"  Vector store query (AI metrics): top result score={results[0].score:.3f} OK")

    # Query for something not in the document
    results = store.query(["quantum computing supply chain"], top_k=3)
    # Should still return results but with lower scores
    print(f"  Vector store query (irrelevant): top result score={results[0].score:.3f} OK")


def test_vector_store_save_load(chunks: list[Chunk]):
    """Test save/load round-trip."""
    store = VectorStore()
    store.build(chunks)

    with tempfile.TemporaryDirectory() as tmpdir:
        store.save(tmpdir)
        store2 = VectorStore()
        store2.load(tmpdir)
        assert store2.index.ntotal == store.index.ntotal
        assert len(store2.chunks) == len(store.chunks)

        # Verify queries work on loaded store
        results = store2.query(["board AI oversight"], top_k=2)
        assert len(results) > 0
    print("  Vector store save/load: OK")


if __name__ == "__main__":
    print("Testing chunk_text...")
    test_chunk_text()
    test_chunk_text_short()

    print("\nTesting XML ingestion...")
    chunks = test_xml_ingestion()

    print("\nTesting vector store...")
    test_vector_store(chunks)
    test_vector_store_save_load(chunks)

    print("\nAll tests passed.")
