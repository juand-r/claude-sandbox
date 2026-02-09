"""
Test the full pipeline wiring with a mock LLM scorer.

This tests everything except the actual API call -- ingest, store, retrieval,
prompt construction, response parsing, aggregation, and report generation.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.indicators import get_all_indicators
from src.scorer import Scorer, IndicatorScore
from src.pipeline import Pipeline, classify_level


# Synthetic XML report with mixed disclosure levels
SAMPLE_REPORT = """<?xml version="1.0" encoding="UTF-8"?>
<report>
    <governance>
        <board_oversight>
            Our Board of Directors has established an AI Ethics Committee under the
            Risk Committee that meets quarterly to review all artificial intelligence
            deployments and associated risks. Board members receive structured AI risk
            reports at each quarterly meeting, with immediate escalation for critical
            incidents. The committee charter explicitly includes oversight of responsible
            AI practices across the organization.
        </board_oversight>
        <board_capability>
            Ms. Sarah Chen, an independent director, brings 15 years of experience in
            machine learning research at Stanford and previously served as CTO at an
            AI safety startup. The board also completed a comprehensive AI literacy
            program in Q2 2024, covering generative AI risks, bias, and regulatory trends.
        </board_capability>
        <ai_policy>
            We published our Responsible AI Framework in March 2024, available on our
            corporate website. The framework is aligned with the EU AI Act risk
            classification, ISO/IEC 42001 AI Management System standard, and Australia's
            eight AI Ethics Principles. It covers fairness, transparency, accountability,
            safety, privacy, and human oversight. The policy is reviewed annually by the
            AI Ethics Committee.
        </ai_policy>
        <sensitive_uses>
            Our policy explicitly prohibits the use of AI for social scoring, real-time
            biometric surveillance in public spaces, and manipulation of vulnerable groups.
            High-risk applications including credit scoring models, automated hiring tools,
            and customer risk profiling require mandatory AI impact assessments and approval
            from the AI Ethics Board before deployment. We maintain a risk-tiered registry
            of all AI systems.
        </sensitive_uses>
    </governance>
    <implementation>
        <rai_responsibility>
            Our Chief AI Officer, Dr. Michael Torres, leads a dedicated Responsible AI
            team of 8 people spanning engineering, legal, and ethics expertise. The team
            reports directly to the CTO and has authority to halt AI deployments that
            fail impact assessments. The team also provides advisory services to product
            teams throughout the development lifecycle.
        </rai_responsibility>
        <employee_training>
            All employees involved in AI development or deployment must complete our
            RAI certification program annually. In 2024, 98% of eligible employees
            (1,247 out of 1,273) completed the certification. The curriculum covers
            bias detection and mitigation, fairness testing methodologies, privacy
            engineering, incident reporting, and regulatory compliance. Senior engineers
            receive additional advanced modules on red-teaming and adversarial robustness.
        </employee_training>
        <system_integration>
            Responsible AI considerations are embedded in our enterprise risk management
            framework under a dedicated AI risk category. All product development follows
            our AI Development Lifecycle (AIDL) which includes mandatory ethics checkpoints
            at design, development, testing, and deployment stages. Our procurement
            policy requires AI vendors to demonstrate compliance with our RAI standards.
            ESG reporting now includes AI-specific metrics.
        </system_integration>
        <incidents>
            We track all AI incidents through our centralized incident management system.
            In 2024, we logged 23 AI-related incidents, down from 34 in 2023 (32% reduction).
            Of these, 3 were classified as high-severity requiring external notification.
            All incidents undergo root cause analysis and findings are reported to the
            AI Ethics Committee. We published an AI Incident Transparency Report for the
            first time in 2024.
        </incidents>
    </implementation>
    <metrics>
        <rai_metrics>
            We now report the following RAI metrics quarterly:
            - Bias audit completion rate: 97% of customer-facing models audited (target: 100%)
            - Fairness score (demographic parity): average 0.92 across models (up from 0.87)
            - AI energy consumption: 14,200 MWh (down 18% YoY through model optimization)
            - AI incident rate: 1.8 per 100 deployments (down from 2.7)
            - Employee RAI certification: 98% completion
            - AI system registry coverage: 100% of production systems catalogued
            These metrics are tied to our published RAI policy commitments and are
            included in our annual sustainability report.
        </rai_metrics>
    </metrics>
    <targets>
        <rai_targets>
            By end of 2025, we aim to achieve 100% bias audit coverage across all
            AI models. We have set a target to reduce AI-related energy consumption
            by 25% per model inference by 2026. Employee RAI certification must maintain
            above 95% annually. We target zero high-severity AI incidents by 2026.
        </rai_targets>
    </targets>
</report>"""


def make_mock_scorer_response(indicator_id: str) -> str:
    """Generate realistic mock LLM responses for each indicator."""
    # This company has strong disclosure across all indicators
    responses = {
        "gov_01": {"score": 5, "evidence": "AI Ethics Committee under Risk Committee, quarterly meetings, structured reporting", "justification": "Comprehensive board accountability with dedicated committee, explicit charter, quarterly cadence.", "disclosed": True},
        "gov_02": {"score": 5, "evidence": "Ms. Sarah Chen with 15 years ML experience, board AI literacy program in Q2 2024", "justification": "Strong board capability with named expert director plus comprehensive board education.", "disclosed": True},
        "gov_03": {"score": 5, "evidence": "Published RAI Framework March 2024, aligned with EU AI Act, ISO 42001, Australia principles", "justification": "Comprehensive public policy with multi-standard alignment and annual review.", "disclosed": True},
        "gov_04": {"score": 5, "evidence": "Prohibited uses listed, mandatory impact assessments for high-risk, risk-tiered registry", "justification": "Exemplary sensitive use governance with prohibitions, tiered review, and system registry.", "disclosed": True},
        "gov_05": {"score": 4, "evidence": "100% bias audit target by 2025, 25% energy reduction by 2026, 95% certification, zero high-severity incidents by 2026", "justification": "Multiple quantified targets with timelines, but some targets are aspirational.", "disclosed": True},
        "gov_06": {"score": 5, "evidence": "Chief AI Officer Dr. Michael Torres, dedicated 8-person RAI team, authority to halt deployments", "justification": "Dedicated named leader with empowered team and real decision authority.", "disclosed": True},
        "gov_07": {"score": 5, "evidence": "98% completion (1247/1273), annual mandatory certification, covers bias/fairness/privacy/incidents", "justification": "Near-universal mandatory program with specific metrics and advanced modules.", "disclosed": True},
        "gov_08": {"score": 5, "evidence": "AI in enterprise risk framework, AIDL with mandatory checkpoints, procurement requirements, ESG integration", "justification": "Comprehensive integration across risk, product dev, procurement, and ESG.", "disclosed": True},
        "gov_09": {"score": 5, "evidence": "23 incidents tracked in 2024, 32% reduction YoY, root cause analysis, public transparency report", "justification": "Full incident management with tracking, external reporting, and published transparency report.", "disclosed": True},
        "gov_10": {"score": 5, "evidence": "Quarterly metrics: bias audit 97%, fairness 0.92, energy 14200 MWh, incident rate 1.8/100", "justification": "Comprehensive metrics dashboard with trend data tied to policy commitments.", "disclosed": True},
    }
    return json.dumps(responses.get(indicator_id, {"score": 0, "evidence": "", "justification": "Unknown indicator", "disclosed": False}))


def test_full_pipeline_with_mock():
    """Test the full pipeline with a mocked LLM."""

    # Write sample report to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(SAMPLE_REPORT)
        filepath = f.name

    pipeline = Pipeline(api_key="fake-key")

    # Mock the Anthropic client
    def mock_score_indicator(self, indicator, results):
        raw = make_mock_scorer_response(indicator.id)
        parsed = json.loads(raw)
        return IndicatorScore(
            indicator_id=indicator.id,
            indicator_name=indicator.name,
            category=indicator.category,
            score=parsed["score"],
            disclosed=parsed["disclosed"],
            evidence=parsed["evidence"],
            justification=parsed["justification"],
            passages_used=len(results),
            source_pages=[r.page for r in results if r.page],
        )

    with patch.object(Scorer, '__init__', lambda self, **kwargs: None):
        with patch.object(Scorer, 'score_indicator', mock_score_indicator):
            report = pipeline.run(filepath)

    # Verify report structure
    assert report.source_file == filepath
    assert report.total_chunks > 0
    assert len(report.indicator_scores) == 10
    assert len(report.categories) == 4  # 4 category groups

    # Verify overall score (all scores are 4 or 5, so avg should be high)
    assert report.overall_score >= 4.0
    assert report.overall_level == "Strong"
    assert report.disclosure_rate == 1.0  # all disclosed

    # Verify category aggregation
    for cat in report.categories:
        assert cat.avg_score > 0
        assert cat.disclosure_rate > 0

    print(f"  Pipeline produced report: overall={report.overall_score}/5 [{report.overall_level}]")
    print(f"  Categories: {len(report.categories)}, Indicators: {len(report.indicator_scores)}")

    # Print the report
    Pipeline.print_report(report)

    # Test JSON serialization
    json_str = Pipeline.report_to_json(report)
    data = json.loads(json_str)
    assert data["overall_score"] == report.overall_score
    assert len(data["indicator_scores"]) == 10
    print("\n  JSON serialization: OK")


def test_classify_level():
    """Test score classification thresholds."""
    assert classify_level(4.5) == "Strong"
    assert classify_level(4.0) == "Strong"
    assert classify_level(3.0) == "Moderate"
    assert classify_level(2.5) == "Moderate"
    assert classify_level(1.5) == "Weak"
    assert classify_level(1.0) == "Weak"
    assert classify_level(0.5) == "Unacceptable"
    assert classify_level(0.0) == "Unacceptable"
    print("  classify_level: OK")


def test_response_parsing():
    """Test the scorer's JSON response parsing handles edge cases."""
    from src.indicators import get_indicator_by_id
    scorer = Scorer.__new__(Scorer)  # skip __init__

    indicator = get_indicator_by_id("gov_01")

    # Normal JSON
    result = scorer._parse_response('{"score": 3, "evidence": "text", "justification": "reason", "disclosed": true}', indicator)
    assert result["score"] == 3
    assert result["disclosed"] is True

    # JSON in markdown code block
    result = scorer._parse_response('```json\n{"score": 4, "evidence": "text", "justification": "reason", "disclosed": true}\n```', indicator)
    assert result["score"] == 4

    # Score out of range (should be clamped)
    result = scorer._parse_response('{"score": 7, "evidence": "", "justification": "", "disclosed": false}', indicator)
    assert result["score"] == 5

    result = scorer._parse_response('{"score": -1, "evidence": "", "justification": "", "disclosed": false}', indicator)
    assert result["score"] == 0

    # Malformed JSON
    result = scorer._parse_response('This is not JSON at all', indicator)
    assert result["score"] == 0
    assert "PARSE ERROR" in result["evidence"]

    print("  Response parsing: all edge cases OK")


if __name__ == "__main__":
    print("Testing classification...")
    test_classify_level()

    print("\nTesting response parsing...")
    test_response_parsing()

    print("\nTesting full pipeline (mock LLM)...")
    test_full_pipeline_with_mock()

    print("\nAll pipeline tests passed.")
