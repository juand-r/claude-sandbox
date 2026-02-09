"""
RAI Indicator Metadata Module

Defines the 10 governance indicators from the CSIRO/Alphinity RAI-ESG Framework,
adapted with ESGReveal-style metadata: search terms, domain knowledge, and
prompt templates for automated extraction.

Each indicator has:
- id: unique identifier
- name: human-readable name
- category: one of Board Oversight, RAI Commitment, RAI Implementation, RAI Metrics
- description: what this indicator assesses
- search_terms: keywords for RAG retrieval (what to search for in documents)
- knowledge: domain expertise to embed in prompts (helps LLM interpret findings)
- rubric: scoring guidance (0-5 Likert scale adapted from CSIRO's binary to granular)
- prompt_template: the extraction/scoring prompt sent to the LLM
"""

from dataclasses import dataclass, field


@dataclass
class Indicator:
    id: str
    name: str
    category: str
    description: str
    search_terms: list[str]
    knowledge: str
    rubric: dict[int, str]
    prompt_template: str


# Standard rubric preamble included in all prompts
RUBRIC_PREAMBLE = """Score this indicator on a 0-5 scale:
0 = Not disclosed: No evidence found in the document.
1 = Minimal: Vague mention without substance (e.g., "we care about responsible AI").
2 = Basic: Some relevant information but lacks specifics or commitments.
3 = Moderate: Reasonably detailed disclosure with some concrete details.
4 = Strong: Detailed disclosure with specific commitments, structures, or metrics.
5 = Comprehensive: Exemplary disclosure with full detail, evidence of implementation, and measurable outcomes.

IMPORTANT: Do not give credit for aspirational language without evidence of action.
A company saying "we are committed to X" with no details scores 1, not 3."""


GOVERNANCE_INDICATORS = [
    Indicator(
        id="gov_01",
        name="Board Accountability",
        category="Board Oversight",
        description=(
            "RAI is explicitly mentioned as part of the responsibility of the Board "
            "or a relevant Board subcommittee (e.g., risk committee, ESG committee). "
            "Structured reporting on AI risks occurs at least annually."
        ),
        search_terms=[
            "board oversight AI",
            "board committee artificial intelligence",
            "board responsibility AI",
            "AI governance board",
            "board AI risk",
            "corporate governance AI",
            "board subcommittee technology",
            "AI oversight committee",
            "board reporting AI",
            "directors AI responsibility",
        ],
        knowledge=(
            "Board-level accountability for AI is a leading indicator of organizational "
            "commitment. Look for: (1) explicit mention of AI in board or committee charters, "
            "(2) named committees with AI oversight responsibility, (3) frequency of AI-related "
            "board reporting. Companies may embed AI oversight in existing risk, audit, or ESG "
            "committees rather than creating dedicated AI committees. General technology oversight "
            "is weaker than specific AI/RAI oversight."
        ),
        rubric={
            0: "No mention of board involvement in AI oversight.",
            1: "Vague reference to board awareness of AI or technology trends.",
            2: "Board mentioned in context of AI but no specific accountability structure.",
            3: "A board committee is identified as having AI oversight, but limited detail on reporting.",
            4: "Clear board/committee accountability for AI with described reporting cadence.",
            5: "Dedicated AI oversight at board level, regular structured reporting, evidence of board engagement with AI risks.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether the company's "
            "Board of Directors has explicit accountability for responsible AI oversight.\n\n"
            "Look for:\n"
            "- Is AI/RAI explicitly part of a board or board committee's mandate?\n"
            "- Is there structured reporting on AI risks to the board?\n"
            "- How frequently does the board review AI matters?\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_02",
        name="Board Capability",
        category="Board Oversight",
        description=(
            "At least one director has strong technology or AI-related experience, "
            "or the board has undertaken AI-specific training/education programs."
        ),
        search_terms=[
            "director technology experience",
            "board AI expertise",
            "director artificial intelligence background",
            "board technology capability",
            "board member tech",
            "director digital experience",
            "board AI training",
            "board education technology",
            "director qualifications technology",
            "board skills matrix AI",
        ],
        knowledge=(
            "Board capability ensures informed oversight. Look for: (1) director biographies "
            "mentioning technology/AI backgrounds, (2) board skills matrices listing AI/technology, "
            "(3) board education or training programs on AI. A former CTO on the board is stronger "
            "evidence than 'directors received a briefing on AI trends.'"
        ),
        rubric={
            0: "No information on board AI/technology capability.",
            1: "General mention of board staying informed about technology.",
            2: "Board skills matrix mentions technology broadly but not AI specifically.",
            3: "At least one director has relevant technology background, or AI training program exists.",
            4: "Director(s) with specific AI/ML experience identified, or comprehensive board AI education program.",
            5: "Multiple directors with deep AI expertise, plus ongoing board education on AI developments.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether the company's "
            "Board of Directors has adequate AI/technology capability.\n\n"
            "Look for:\n"
            "- Directors with technology, AI, or data science backgrounds\n"
            "- Board skills matrices mentioning AI or advanced technology\n"
            "- Board training or education programs on AI\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_03",
        name="Public RAI Policy",
        category="RAI Commitment",
        description=(
            "A publicly available responsible AI policy or framework, aligned with recognized "
            "standards (EU AI Act, ISO/IEC 42001, national AI ethics principles). "
            "Addresses ethics, testing, transparency."
        ),
        search_terms=[
            "responsible AI policy",
            "AI ethics policy",
            "AI principles",
            "responsible AI framework",
            "ethical AI guidelines",
            "AI governance policy",
            "AI ethics principles",
            "responsible use of AI",
            "AI policy public",
            "trustworthy AI framework",
        ],
        knowledge=(
            "A public RAI policy signals commitment and accountability. Only 10% of companies "
            "publicly disclose RAI policies (CSIRO finding). Look for: (1) a named document/policy, "
            "(2) whether it's publicly available vs internal-only, (3) alignment with standards "
            "(EU AI Act, NIST, ISO 42001, OECD), (4) whether it covers ethics, testing/validation, "
            "and transparency. Internal-only policies score lower than public ones."
        ),
        rubric={
            0: "No mention of any AI policy or principles.",
            1: "Vague statement about responsible AI commitment with no policy details.",
            2: "Internal AI guidelines mentioned but not publicly available.",
            3: "Public AI principles or policy exists, covers some key areas.",
            4: "Detailed public RAI policy aligned with recognized standards, covering ethics, testing, transparency.",
            5: "Comprehensive public RAI framework with standard alignment, regular review cycles, and evidence of enforcement.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether the company "
            "has a public Responsible AI policy or framework.\n\n"
            "Look for:\n"
            "- Named AI ethics/responsibility policy or principles document\n"
            "- Whether the policy is publicly available\n"
            "- Alignment with standards (EU AI Act, ISO 42001, NIST, OECD)\n"
            "- Coverage of ethics, testing/validation, and transparency\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_04",
        name="Sensitive Use Cases",
        category="RAI Commitment",
        description=(
            "High-risk AI applications (facial recognition, biometrics, credit scoring, "
            "hiring algorithms) are explicitly addressed in policy with additional oversight."
        ),
        search_terms=[
            "high risk AI",
            "facial recognition policy",
            "biometric AI",
            "AI use cases restricted",
            "prohibited AI uses",
            "sensitive AI applications",
            "AI risk classification",
            "high-risk artificial intelligence",
            "AI prohibited uses",
            "restricted AI deployment",
        ],
        knowledge=(
            "Addressing sensitive use cases shows maturity beyond generic commitments. "
            "Look for: (1) explicit lists of high-risk or prohibited AI uses, (2) enhanced "
            "review/approval for sensitive deployments, (3) alignment with EU AI Act risk "
            "categories. Companies that only talk about AI benefits without acknowledging "
            "sensitive uses score low."
        ),
        rubric={
            0: "No mention of high-risk or sensitive AI applications.",
            1: "General acknowledgment that AI can have risks, no specific use cases.",
            2: "Some sensitive use cases mentioned but no specific policies for them.",
            3: "High-risk use cases identified with some additional governance described.",
            4: "Clear policy on sensitive/restricted AI uses with approval processes.",
            5: "Comprehensive sensitive use framework with prohibited uses list, tiered review, and ongoing monitoring.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether the company "
            "explicitly addresses high-risk or sensitive AI use cases.\n\n"
            "Look for:\n"
            "- Lists of high-risk, restricted, or prohibited AI uses\n"
            "- Enhanced review/approval processes for sensitive AI deployments\n"
            "- Risk classification of AI applications\n"
            "- Mentions of facial recognition, biometrics, automated decision-making in hiring/credit\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_05",
        name="RAI Target",
        category="RAI Commitment",
        description=(
            "Clear, measurable RAI objectives such as workforce training targets, "
            "incident reduction goals, bias audit completion rates."
        ),
        search_terms=[
            "AI target",
            "AI training target",
            "responsible AI goals",
            "AI metrics target",
            "AI KPI",
            "AI workforce training",
            "AI incident reduction",
            "AI audit target",
            "measurable AI objectives",
            "responsible AI milestones",
        ],
        knowledge=(
            "Targets distinguish real commitment from aspirational statements. "
            "Look for: (1) quantified objectives (e.g., '100% of AI developers trained by 2025'), "
            "(2) measurable goals tied to RAI policy, (3) timelines attached to AI-related targets. "
            "Targets like 'reduce AI incidents' without a number or timeline score lower than "
            "'reduce AI incidents by 50% by 2025.'"
        ),
        rubric={
            0: "No RAI-related targets or goals mentioned.",
            1: "General aspiration to improve AI practices, no measurable targets.",
            2: "Some goals stated but not quantified or time-bound.",
            3: "At least one measurable RAI target with timeline.",
            4: "Multiple measurable targets covering different RAI dimensions.",
            5: "Comprehensive target framework with quantified objectives, timelines, and progress reporting.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether the company "
            "has clear, measurable Responsible AI targets.\n\n"
            "Look for:\n"
            "- Quantified AI-related objectives (percentages, counts, dates)\n"
            "- Targets for AI training, bias audits, incident reduction\n"
            "- Timelines attached to AI goals\n"
            "- Progress reporting against targets\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_06",
        name="Dedicated RAI Responsibility",
        category="RAI Implementation",
        description=(
            "A designated officer, function, or team responsible for overseeing "
            "responsible AI practices (e.g., Chief AI Officer, RAI team, AI ethics board)."
        ),
        search_terms=[
            "chief AI officer",
            "AI ethics officer",
            "responsible AI team",
            "AI governance team",
            "head of AI",
            "AI ethics board",
            "AI oversight role",
            "AI responsibility officer",
            "dedicated AI function",
            "AI governance role",
        ],
        knowledge=(
            "Dedicated responsibility signals organizational investment. Look for: "
            "(1) named roles (Chief AI Officer, Head of AI Ethics), (2) dedicated teams or "
            "functions, (3) cross-functional AI ethics committees/boards. AI responsibility "
            "embedded in existing CTO/CDO roles is weaker than a dedicated function. "
            "An advisory board with no decision-making power is weaker than an empowered team."
        ),
        rubric={
            0: "No dedicated AI responsibility mentioned.",
            1: "AI responsibility vaguely assigned ('our technology team handles this').",
            2: "AI oversight is part of an existing role (CTO, CDO) but not primary responsibility.",
            3: "Named role or team with AI oversight as a significant responsibility.",
            4: "Dedicated AI ethics/responsibility role or team with clear mandate.",
            5: "Dedicated function with named leadership, cross-functional reach, and decision authority.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether the company "
            "has dedicated responsibility for Responsible AI.\n\n"
            "Look for:\n"
            "- Named AI officer roles (Chief AI Officer, AI Ethics Officer)\n"
            "- Dedicated AI ethics/governance teams\n"
            "- Cross-functional AI ethics committees or boards\n"
            "- Clear mandate and decision-making authority\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_07",
        name="Employee Awareness",
        category="RAI Implementation",
        description=(
            "Formal programs addressing AI ethics, responsible AI practices, and ESG "
            "considerations for employees involved in AI development or deployment."
        ),
        search_terms=[
            "AI ethics training",
            "AI training employees",
            "responsible AI training",
            "AI awareness program",
            "AI education workforce",
            "AI ethics education",
            "employee AI training",
            "AI skills development",
            "AI literacy program",
            "responsible AI education",
        ],
        knowledge=(
            "Employee awareness is essential because frontline teams make daily decisions "
            "about AI implementation. Look for: (1) formal training programs (not just a talk), "
            "(2) coverage of AI ethics, not just technical AI skills, (3) participation rates "
            "or completion metrics, (4) mandatory vs optional programs. 'We encourage employees "
            "to learn about AI' is much weaker than 'all AI developers complete our RAI "
            "certification program.'"
        ),
        rubric={
            0: "No mention of AI-related employee training or awareness.",
            1: "General mention of employee awareness with no program details.",
            2: "Some AI training exists but focused on technical skills, not ethics/responsibility.",
            3: "RAI-specific training program exists with some detail on content.",
            4: "Structured RAI training with described curriculum, audience, and participation data.",
            5: "Comprehensive mandatory RAI training with completion metrics, regular updates, role-specific content.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess the company's "
            "employee awareness and training programs for Responsible AI.\n\n"
            "Look for:\n"
            "- Formal AI ethics or RAI training programs\n"
            "- Who is required to complete training (all employees, AI teams, etc.)\n"
            "- Training content covering ethics, not just technical AI skills\n"
            "- Participation rates or completion metrics\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_08",
        name="System Integration",
        category="RAI Implementation",
        description=(
            "RAI practices embedded in existing organizational systems: risk management, "
            "product development, procurement, and ESG processes."
        ),
        search_terms=[
            "AI risk management",
            "AI product development process",
            "AI procurement policy",
            "AI impact assessment",
            "AI risk framework",
            "AI development lifecycle",
            "AI due diligence",
            "AI supply chain",
            "responsible AI integration",
            "AI risk assessment process",
        ],
        knowledge=(
            "Integration into existing systems matters more than standalone AI policies. "
            "Look for: (1) AI in enterprise risk management frameworks, (2) AI review gates "
            "in product development, (3) AI requirements in procurement/vendor assessment, "
            "(4) AI considerations in ESG reporting processes. A company that treats AI risk "
            "as part of its standard risk taxonomy is more mature than one with a separate "
            "AI ethics document that isn't connected to operational processes."
        ),
        rubric={
            0: "No evidence of RAI integration into organizational systems.",
            1: "AI mentioned in risk context but not integrated into formal processes.",
            2: "AI included in one system (e.g., risk management) but not others.",
            3: "AI integrated into 2+ organizational systems with some detail.",
            4: "AI systematically embedded in risk, product development, and at least one other process.",
            5: "Comprehensive integration across risk, product dev, procurement, and ESG with evidence of functioning processes.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess whether Responsible AI "
            "practices are integrated into the company's organizational systems.\n\n"
            "Look for:\n"
            "- AI in enterprise risk management frameworks\n"
            "- AI review gates in product development lifecycle\n"
            "- AI requirements in procurement or vendor assessment\n"
            "- AI considerations in ESG/sustainability reporting\n"
            "- AI impact assessments as part of standard processes\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_09",
        name="AI Incidents Management",
        category="RAI Implementation",
        description=(
            "Internal tracking system for AI-related incidents with external reporting "
            "of serious incidents."
        ),
        search_terms=[
            "AI incident",
            "AI incident reporting",
            "AI incident management",
            "AI failure reporting",
            "AI error tracking",
            "AI safety incident",
            "AI harm reporting",
            "AI bias incident",
            "AI issue tracking",
            "AI problem reporting",
        ],
        knowledge=(
            "Incident management is often the weakest area. Look for: (1) defined process "
            "for identifying and reporting AI incidents, (2) internal tracking systems, "
            "(3) external disclosure of serious incidents, (4) post-incident review processes. "
            "Companies rarely disclose AI incidents voluntarily. Even acknowledging that incident "
            "tracking exists is a positive signal. Generic IT incident management that doesn't "
            "specifically address AI is weaker evidence."
        ),
        rubric={
            0: "No mention of AI incident tracking or reporting.",
            1: "General incident management mentioned, AI not specifically addressed.",
            2: "AI incidents acknowledged as a concern but no formal process described.",
            3: "Internal AI incident tracking process exists with some detail.",
            4: "Structured AI incident management with defined severity levels and response procedures.",
            5: "Comprehensive AI incident framework with internal tracking, external reporting, post-incident review, and disclosed incident metrics.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess the company's "
            "AI incident management practices.\n\n"
            "Look for:\n"
            "- Defined processes for identifying AI-related incidents\n"
            "- Internal tracking systems for AI failures, biases, or harms\n"
            "- External reporting or disclosure of AI incidents\n"
            "- Post-incident review and remediation processes\n"
            "- Any disclosed incident metrics or statistics\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
    Indicator(
        id="gov_10",
        name="RAI Metrics Disclosure",
        category="RAI Metrics",
        description=(
            "Externally reported metrics associated with RAI policy commitments, "
            "such as bias audit results, model performance data, energy usage of AI systems."
        ),
        search_terms=[
            "AI metrics",
            "AI performance metrics",
            "AI bias audit results",
            "AI energy consumption",
            "AI model accuracy",
            "AI fairness metrics",
            "responsible AI metrics",
            "AI KPI results",
            "AI transparency metrics",
            "AI environmental impact",
        ],
        knowledge=(
            "Metrics disclosure is the highest bar: it requires not just policies and processes "
            "but actual measurement and external reporting. Look for: (1) quantified metrics "
            "tied to RAI commitments, (2) bias/fairness audit results, (3) AI energy/carbon "
            "metrics, (4) model performance data shared externally. This is the rarest disclosure "
            "type. Even partial metrics (e.g., reporting AI energy usage) are significant."
        ),
        rubric={
            0: "No RAI metrics disclosed.",
            1: "Mention of measuring AI impacts with no actual metrics provided.",
            2: "One or two basic metrics mentioned without much detail.",
            3: "Several RAI metrics reported with reasonable detail.",
            4: "Comprehensive metrics covering multiple RAI dimensions with trend data.",
            5: "Full metrics dashboard covering fairness, performance, environmental impact, with year-over-year tracking and targets.",
        },
        prompt_template=(
            "Based on the following passages from a corporate report, assess the company's "
            "disclosure of Responsible AI metrics.\n\n"
            "Look for:\n"
            "- Quantified metrics tied to AI responsibility (bias rates, fairness scores)\n"
            "- AI system performance data (accuracy, reliability)\n"
            "- AI environmental metrics (energy use, carbon footprint of AI)\n"
            "- Trend data or year-over-year comparisons\n"
            "- Metrics tied to specific RAI policy commitments\n\n"
            "{rubric}\n\n"
            "PASSAGES:\n{passages}\n\n"
            "Respond in this exact JSON format:\n"
            '{{"score": <0-5>, "evidence": "<direct quotes or specific references>", '
            '"justification": "<why this score>", "disclosed": <true/false>}}'
        ),
    ),
]


def get_all_indicators() -> list[Indicator]:
    """Return all governance indicators."""
    return GOVERNANCE_INDICATORS


def get_indicator_by_id(indicator_id: str) -> Indicator | None:
    """Look up an indicator by its ID."""
    for ind in GOVERNANCE_INDICATORS:
        if ind.id == indicator_id:
            return ind
    return None


def get_indicators_by_category(category: str) -> list[Indicator]:
    """Return indicators in a given category."""
    return [ind for ind in GOVERNANCE_INDICATORS if ind.category == category]
