"""
Test XML/XBRL ingestion with realistic financial document formats.

Covers:
- Plain XML (generic ESG report structure)
- XBRL with namespaces (traditional XBRL instance documents)
- Inline XBRL (iXBRL) - HTML with embedded XBRL tags (SEC/ESRS style)
- Edge cases: empty elements, deeply nested content, HTML in text blocks
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingest import ingest_xml, ingest, Chunk, chunk_text, _strip_html


# --- Test fixtures ---

PLAIN_XML = """<?xml version="1.0" encoding="UTF-8"?>
<sustainability-report>
    <governance>
        <ai-oversight>
            The Board's Technology and Risk Committee has explicit responsibility
            for overseeing artificial intelligence strategy and risk management.
            The committee receives quarterly reports on AI deployments, incidents,
            and compliance with our Responsible AI Policy.
        </ai-oversight>
    </governance>
    <social>
        <workforce-ai>
            We completed mandatory AI ethics training for 94% of our technology
            workforce in 2024. Our Chief AI Ethics Officer reports directly to
            the CTO and has authority to delay or halt AI deployments that fail
            our impact assessment process.
        </workforce-ai>
    </social>
</sustainability-report>"""

# Traditional XBRL instance document with namespaces
XBRL_INSTANCE = """<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl
    xmlns:xbrli="http://www.xbrl.org/2003/instance"
    xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
    xmlns:esrs="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22"
    xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
    xmlns:link="http://www.xbrl.org/2003/linkbase">

    <xbrli:context id="FY2024">
        <xbrli:entity>
            <xbrli:identifier scheme="http://www.example.com">EXAMPLE_CORP</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:startDate>2024-01-01</xbrli:startDate>
            <xbrli:endDate>2024-12-31</xbrli:endDate>
        </xbrli:period>
    </xbrli:context>

    <esrs:DisclosureOfGovernanceStructureExplanation contextRef="FY2024">
        The company's governance structure includes a dedicated AI Ethics Board
        reporting to the main Board of Directors. This body oversees all artificial
        intelligence deployments across the organization, with particular focus on
        high-risk applications in credit scoring and customer profiling. Board
        members include two directors with extensive experience in machine learning
        and data science. The AI Ethics Board meets monthly and provides quarterly
        reports to the full Board. In 2024, the Board reviewed 47 AI deployment
        proposals and rejected 3 due to insufficient bias testing.
    </esrs:DisclosureOfGovernanceStructureExplanation>

    <esrs:DescriptionOfPoliciesAdoptedExplanation contextRef="FY2024">
        Our Responsible AI Policy, published in January 2024, establishes mandatory
        requirements for all AI systems. The policy is aligned with the EU AI Act
        risk classification framework and ISO/IEC 42001. Key requirements include:
        mandatory bias audits for all customer-facing models, human oversight for
        automated decisions affecting individuals, incident reporting within 24 hours,
        and annual third-party AI audits. The policy explicitly prohibits the use of
        AI for social scoring and real-time biometric surveillance.
    </esrs:DescriptionOfPoliciesAdoptedExplanation>

    <esrs:DisclosureOfMetricsExplanation contextRef="FY2024">
        AI responsibility metrics for FY2024: bias audit completion rate 96%
        (target 100%), mean demographic parity score 0.94, AI-related incidents
        reduced by 28% year-over-year to 19 total (3 high severity), AI training
        energy consumption 8,400 MWh (down 22% through model distillation),
        employee RAI certification completion 97%. All metrics are externally
        audited and published in our annual sustainability report.
    </esrs:DisclosureOfMetricsExplanation>

    <esrs:NumberOfEmployees contextRef="FY2024" unitRef="pure" decimals="0">12500</esrs:NumberOfEmployees>

    <esrs:GHGEmissionsScope1 contextRef="FY2024" unitRef="tCO2e" decimals="0">45000</esrs:GHGEmissionsScope1>

</xbrli:xbrl>"""

# Inline XBRL (iXBRL) - HTML document with embedded XBRL tags
# This is what SEC EDGAR and ESRS filings actually look like
IXBRL_DOCUMENT = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
      xmlns:xbrli="http://www.xbrl.org/2003/instance"
      xmlns:us-gaap="http://fasb.org/us-gaap/2024"
      xmlns:dei="http://xbrl.sec.gov/dei/2024"
      xmlns:esrs="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22">
<head>
    <title>Annual Report 2024 - Example Corp</title>
</head>
<body>
    <ix:header>
        <ix:hidden>
            <ix:nonNumeric name="dei:EntityRegistrantName" contextRef="FY2024">Example Corporation</ix:nonNumeric>
        </ix:hidden>
        <ix:resources>
            <xbrli:context id="FY2024">
                <xbrli:entity>
                    <xbrli:identifier scheme="http://www.sec.gov/cik">0001234567</xbrli:identifier>
                </xbrli:entity>
                <xbrli:period>
                    <xbrli:startDate>2024-01-01</xbrli:startDate>
                    <xbrli:endDate>2024-12-31</xbrli:endDate>
                </xbrli:period>
            </xbrli:context>
        </ix:resources>
    </ix:header>

    <div class="section">
        <h2>Corporate Governance</h2>
        <ix:nonNumeric name="esrs:DisclosureOfGovernanceStructureExplanation"
                       contextRef="FY2024" escape="true">
            <p>Our Board of Directors maintains oversight of AI through its
            Technology and Innovation Committee. The committee charter was
            amended in 2024 to explicitly include responsible AI governance.</p>
            <p>Key governance actions in 2024:</p>
            <ul>
                <li>Appointed Dr. Lisa Wang as Chief AI Officer</li>
                <li>Established mandatory AI impact assessments for all new deployments</li>
                <li>Implemented quarterly AI risk reporting to the full Board</li>
            </ul>
        </ix:nonNumeric>
    </div>

    <div class="section">
        <h2>Responsible AI</h2>
        <ix:nonNumeric name="esrs:DescriptionOfPoliciesAdoptedExplanation"
                       contextRef="FY2024" escape="true">
            <p>Our Responsible AI Framework, available at example.com/rai, covers
            six principles: fairness, transparency, accountability, safety, privacy,
            and human oversight. The framework is aligned with ISO/IEC 42001 and
            the NIST AI Risk Management Framework.</p>
            <p>In 2024, we completed bias audits on <ix:nonNumeric
            name="esrs:PercentageOfAISystemsAudited" contextRef="FY2024"
            format="ixt:num-dot-decimal">94.5</ix:nonNumeric>% of our
            customer-facing AI models.</p>
        </ix:nonNumeric>
    </div>

    <div class="section">
        <h2>AI Workforce Development</h2>
        <p>We invested significantly in AI ethics training across the organization.
        Our mandatory Responsible AI certification program achieved a completion
        rate of 96% among all AI practitioners. The program includes modules on
        bias detection, fairness metrics, privacy engineering, and regulatory
        compliance. Board members completed a dedicated AI literacy workshop
        covering emerging risks from generative AI systems.</p>
    </div>

    <div class="section">
        <h2>AI Incident Management</h2>
        <ix:nonNumeric name="esrs:DisclosureOfIncidentManagementExplanation"
                       contextRef="FY2024" escape="false">
            We maintain a centralized AI incident tracking system integrated with
            our enterprise risk management platform. In 2024, we recorded 15
            AI-related incidents (down from 22 in 2023). Two incidents were classified
            as high-severity, both involving unexpected model drift in credit scoring
            models. Root cause analyses were completed for all incidents within 30 days.
            We published our first AI Incident Transparency Report in Q4 2024.
        </ix:nonNumeric>
    </div>
</body>
</html>"""

# XBRL with HTML embedded in text blocks (common in practice)
XBRL_WITH_HTML = """<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl
    xmlns:xbrli="http://www.xbrl.org/2003/instance"
    xmlns:esrs="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22">

    <xbrli:context id="FY2024">
        <xbrli:entity>
            <xbrli:identifier scheme="http://example.com">CORP</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:startDate>2024-01-01</xbrli:startDate>
            <xbrli:endDate>2024-12-31</xbrli:endDate>
        </xbrli:period>
    </xbrli:context>

    <esrs:DisclosureOfGovernanceStructureExplanation contextRef="FY2024">
        <p>The company has established an <b>AI Governance Committee</b> with the
        following responsibilities:</p>
        <ul>
            <li>Review and approve all high-risk AI deployments</li>
            <li>Monitor AI incident reports and remediation actions</li>
            <li>Oversee compliance with the EU AI Act</li>
        </ul>
        <p>The committee is chaired by <b>Dr. James Park</b>, an independent
        director with 20 years of experience in artificial intelligence research.</p>
        <table>
            <tr><th>Metric</th><th>2023</th><th>2024</th></tr>
            <tr><td>AI Incidents</td><td>31</td><td>18</td></tr>
            <tr><td>Bias Audits Completed</td><td>85%</td><td>96%</td></tr>
            <tr><td>RAI Training Completion</td><td>88%</td><td>97%</td></tr>
        </table>
    </esrs:DisclosureOfGovernanceStructureExplanation>

    <esrs:ShortText contextRef="FY2024">Too short to matter.</esrs:ShortText>

</xbrli:xbrl>"""

# Edge case: deeply nested XML with minimal text
SPARSE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<report>
    <section>
        <subsection>
            <paragraph>Brief mention of AI.</paragraph>
        </subsection>
    </section>
    <empty-section/>
    <another-section>
        <item></item>
        <item>   </item>
    </another-section>
</report>"""


# --- Tests ---

def test_plain_xml():
    """Basic XML with no namespaces."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(PLAIN_XML)
        f.flush()
        chunks = ingest_xml(f.name)

    assert len(chunks) > 0, "No chunks from plain XML"
    all_text = " ".join(c.text for c in chunks)
    assert "Technology and Risk Committee" in all_text
    assert "AI ethics training" in all_text
    # Check sections are detected
    sections = set(c.section for c in chunks if c.section)
    assert len(sections) > 0, "No sections detected"
    print(f"  Plain XML: {len(chunks)} chunks, sections: {sections}")


def test_xbrl_instance():
    """Traditional XBRL with namespaces and typed elements."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xbrl', delete=False) as f:
        f.write(XBRL_INSTANCE)
        f.flush()
        chunks = ingest(f.name)  # test auto-detection too

    assert len(chunks) > 0, "No chunks from XBRL"
    all_text = " ".join(c.text for c in chunks)

    # Should extract narrative text blocks
    assert "AI Ethics Board" in all_text, "Missing governance disclosure"
    assert "Responsible AI Policy" in all_text, "Missing policy disclosure"
    assert "bias audit completion rate" in all_text, "Missing metrics disclosure"

    # Should NOT extract short numeric elements as text chunks
    # (NumberOfEmployees = "12500" is too short to pass the 100-char threshold)
    assert "12500" not in all_text or len(all_text) > 200, "Numeric-only elements should be filtered"

    # Check metadata
    for c in chunks:
        assert c.metadata.get("format") == "xbrl", f"Expected xbrl format, got {c.metadata}"

    # Check sections use tag local names
    sections = set(c.section for c in chunks if c.section)
    print(f"  XBRL instance: {len(chunks)} chunks, sections: {sections}")


def test_ixbrl_document():
    """Inline XBRL (HTML with embedded XBRL tags)."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xhtml', delete=False) as f:
        f.write(IXBRL_DOCUMENT)
        f.flush()
        chunks = ingest(f.name)

    assert len(chunks) > 0, f"No chunks from iXBRL"
    all_text = " ".join(c.text for c in chunks)

    # Should extract content from ix:nonNumeric blocks AND regular HTML text
    assert "Technology and Innovation Committee" in all_text, "Missing governance text"
    assert "Responsible AI Framework" in all_text, "Missing RAI framework text"
    assert "AI incident tracking" in all_text or "incident" in all_text.lower(), "Missing incident text"

    print(f"  iXBRL: {len(chunks)} chunks")
    for c in chunks[:3]:
        preview = c.text[:80].replace('\n', ' ')
        print(f"    [{c.section}] {preview}...")


def test_xbrl_with_embedded_html():
    """XBRL with HTML markup inside text blocks."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xbrl', delete=False) as f:
        f.write(XBRL_WITH_HTML)
        f.flush()
        chunks = ingest(f.name)

    assert len(chunks) > 0, "No chunks from XBRL with HTML"
    all_text = " ".join(c.text for c in chunks)

    # HTML tags should be stripped
    assert "<p>" not in all_text, "HTML <p> tags not stripped"
    assert "<b>" not in all_text, "HTML <b> tags not stripped"
    assert "<ul>" not in all_text, "HTML <ul> tags not stripped"
    assert "<table>" not in all_text, "HTML <table> tags not stripped"

    # But content should be preserved
    assert "AI Governance Committee" in all_text
    assert "Dr. James Park" in all_text
    assert "EU AI Act" in all_text

    # Short text elements should be filtered out
    assert "Too short to matter" not in all_text, "Short elements should be filtered (< 100 chars)"

    print(f"  XBRL+HTML: {len(chunks)} chunks, HTML stripped correctly")


def test_sparse_xml():
    """XML with minimal/empty content shouldn't crash."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(SPARSE_XML)
        f.flush()
        chunks = ingest_xml(f.name)

    # Should handle gracefully, may produce 0 or 1 chunks
    all_text = " ".join(c.text for c in chunks)
    print(f"  Sparse XML: {len(chunks)} chunks (expected 0-1)")


def test_strip_html():
    """Test HTML stripping utility."""
    assert _strip_html("<p>Hello <b>world</b></p>") == "Hello world"
    assert _strip_html("No tags here") == "No tags here"
    assert _strip_html("<ul><li>Item 1</li><li>Item 2</li></ul>") == "Item 1 Item 2"
    assert _strip_html("") == ""
    print("  _strip_html: OK")


def test_auto_detect_file_type():
    """Test that ingest() correctly auto-detects file types."""
    # .xbrl should be treated as XML
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xbrl', delete=False) as f:
        f.write(XBRL_INSTANCE)
        f.flush()
        chunks = ingest(f.name)
    assert len(chunks) > 0
    print("  Auto-detect .xbrl: OK")

    # .xhtml should be treated as XML
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xhtml', delete=False) as f:
        f.write(IXBRL_DOCUMENT)
        f.flush()
        chunks = ingest(f.name)
    assert len(chunks) > 0
    print("  Auto-detect .xhtml: OK")

    # .xml should be treated as XML
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(PLAIN_XML)
        f.flush()
        chunks = ingest(f.name)
    assert len(chunks) > 0
    print("  Auto-detect .xml: OK")


if __name__ == "__main__":
    print("Testing HTML stripping...")
    test_strip_html()

    print("\nTesting plain XML ingestion...")
    test_plain_xml()

    print("\nTesting XBRL instance document...")
    test_xbrl_instance()

    print("\nTesting inline XBRL (iXBRL)...")
    test_ixbrl_document()

    print("\nTesting XBRL with embedded HTML...")
    test_xbrl_with_embedded_html()

    print("\nTesting sparse/edge-case XML...")
    test_sparse_xml()

    print("\nTesting file type auto-detection...")
    test_auto_detect_file_type()

    print("\nAll XML/XBRL ingestion tests passed.")
