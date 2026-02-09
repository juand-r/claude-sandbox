# XBRL/iXBRL for ESG & Sustainability Reporting - Technical Reference

Research compiled 2026-02-09 from SEC EDGAR, EFRAG, XBRL International, IFRS Foundation sources.

---

## 1. Real XBRL Namespaces

### SEC EDGAR (US Financial Reporting)

```xml
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
  xmlns:ixt="http://www.xbrl.org/inlineXBRL/transformation/2020-02-12"
  xmlns:ixt-sec="http://www.sec.gov/inlineXBRL/transformation/2015-08-31"
  xmlns:xbrli="http://www.xbrl.org/2003/instance"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:link="http://www.xbrl.org/2003/linkbase"
  xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
  xmlns:us-gaap="http://fasb.org/us-gaap/2024"
  xmlns:dei="http://xbrl.sec.gov/dei/2024"
  xmlns:srt="http://fasb.org/srt/2024"
  xmlns:ecd="http://xbrl.sec.gov/ecd/2024"
  xmlns:country="http://xbrl.sec.gov/country/2024"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:aapl="http://www.apple.com/20241228"
>
```

Key namespace notes:
- `ix:` = Inline XBRL elements (v1.1 uses `http://www.xbrl.org/2013/inlineXBRL`)
- `ixt:` = Transformation rules for formatting
- `us-gaap:` = US GAAP taxonomy (versioned annually by FASB)
- `dei:` = Document and Entity Information (SEC-specific metadata)
- `srt:` = SEC Reporting Taxonomy
- Company-specific extension namespace (e.g., `aapl:`) for custom elements

### ESRS (European Sustainability Reporting Standards)

```xml
xmlns:esrs="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22"
```

- Taxonomy entry point: `https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_all.xsd`
- Core schema: `https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/common/esrs_cor.xsd`
- Prefix: **`esrs:`**
- Published by EFRAG, August 2024. Basis for ESMA's RTS for CSRD digital tagging.

### IFRS Sustainability Disclosure Taxonomy (ISSB)

```xml
xmlns:ifrs-sds="http://xbrl.ifrs.org/taxonomy/2024/ifrs-sds"
```

- Covers IFRS S1 (General Requirements) and IFRS S2 (Climate-related Disclosures)
- Uses architecture consistent with `ifrs-full:` accounting taxonomy
- Published April 2024 by ISSB

### GRI Sustainability Taxonomy

```xml
xmlns:gri="http://xbrl.globalreporting.org/taxonomy/2025"
```

- Launched June 2025, covering all GRI Standards (Universal, Sector, Topic)
- First global ESG standard-setter with full XBRL framework
- Designed for interoperability with ESRS and ISSB taxonomies

---

## 2. How Narrative/Textual Disclosures Are Encoded in XBRL

### Core Concept: `ix:nonNumeric` vs `ix:nonFraction`

XBRL facts are either:
- **Numeric**: tagged with `ix:nonFraction` (monetary amounts, percentages, counts)
- **Non-numeric**: tagged with `ix:nonNumeric` (text, dates, booleans, narrative blocks)

For ESG/sustainability reports, **60-70% of all datapoints are narrative disclosures**. These are the primary extraction targets.

### Data Types for Text

| XBRL Data Type | Usage | `escape` attribute |
|---|---|---|
| `xbrli:stringItemType` | Short text values (names, identifiers) | `escape="false"` |
| `dtr-types:textBlockItemType` | Long narrative blocks with formatting (HTML) | `escape="true"` |
| `xbrli:booleanItemType` | Yes/No flags | N/A |
| `enum2:enumerationItemType` | Multiple-choice / single-choice values | N/A |

### The `escape` Attribute - Critical Distinction

**`escape="false"` (default):** Only text content is extracted. HTML tags are stripped.

```xml
<ix:nonNumeric contextRef="c1" name="dei:EntityRegistrantName" escape="false">
  <span style="font-weight:bold;">Apple Inc.</span>
</ix:nonNumeric>
<!-- Extracted XBRL fact value: "Apple Inc." (plain text) -->
```

**`escape="true"`:** HTML markup is preserved in the fact value as escaped XHTML.

```xml
<ix:nonNumeric contextRef="c20240101_20241231"
               name="us-gaap:SignificantAccountingPoliciesTextBlock"
               id="fact-sig-acct-pol"
               escape="true">
  <div style="margin-top:6pt;">
    <p style="font-size:10pt;font-family:'Times New Roman';">
      <span style="font-weight:bold;">Note 1 - Summary of Significant Accounting Policies</span>
    </p>
    <p style="font-size:10pt;font-family:'Times New Roman';">
      The Company accounts for its investments in accordance with ASC 320...
    </p>
  </div>
</ix:nonNumeric>
<!-- Extracted XBRL fact value: the full HTML as escaped XHTML fragment -->
```

**Rule:** Facts using `dtr-types:textBlockItemType` MUST use `escape="true"`. The resulting fact value MUST be valid XHTML.

### ESRS Tagging Hierarchy for Narratives

The ESRS taxonomy uses a 3-level nesting scheme for narrative disclosures:

- **Level 1 (Parent):** Entire Disclosure Requirement as a single textBlock
  - e.g., `esrs:DisclosureOfTransitionPlanForClimateChangeMitigationExplanation`
- **Level 2 (Children):** Specific datapoints within the DR
  - e.g., `esrs:DescriptionOfDecarbonisationLevers`
- **Level 3 (Grandchildren):** Roman-numbered sub-items
  - e.g., `esrs:DescriptionOfKeyAssumptionsUsedInTransitionPlan`

---

## 3. What Inline XBRL (iXBRL) Looks Like

### Complete Realistic iXBRL Document Structure (SEC 10-K Style)

```html
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
      xmlns:ixt="http://www.xbrl.org/inlineXBRL/transformation/2020-02-12"
      xmlns:xbrli="http://www.xbrl.org/2003/instance"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xmlns:link="http://www.xbrl.org/2003/linkbase"
      xmlns:us-gaap="http://fasb.org/us-gaap/2024"
      xmlns:dei="http://xbrl.sec.gov/dei/2024"
      xmlns:srt="http://fasb.org/srt/2024"
      xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
      xmlns:acme="http://www.acmecorp.com/20241231"
      xml:lang="en-US">
<head>
  <title>ACME Corp 10-K</title>
</head>
<body>

<!-- === XBRL HEADER (hidden metadata) === -->
<ix:header>
  <ix:hidden>
    <!-- Hidden non-displayed facts (metadata) -->
    <ix:nonNumeric contextRef="c_entity"
                   name="dei:EntityCentralIndexKey">0001234567</ix:nonNumeric>
    <ix:nonNumeric contextRef="c_entity"
                   name="dei:DocumentType">10-K</ix:nonNumeric>
    <ix:nonNumeric contextRef="c_entity"
                   name="dei:DocumentPeriodEndDate"
                   format="ixt:date-monthname-day-year-en">December 31, 2024</ix:nonNumeric>
    <ix:nonNumeric contextRef="c_entity"
                   name="dei:EntityFileNumber">001-12345</ix:nonNumeric>
    <ix:nonNumeric contextRef="c_entity"
                   name="dei:CurrentFiscalYearEndDate">--12-31</ix:nonNumeric>
    <ix:nonNumeric contextRef="c_entity"
                   name="dei:AmendmentFlag">false</ix:nonNumeric>
  </ix:hidden>

  <ix:references>
    <link:schemaRef xlink:type="simple"
                    xlink:href="acme-20241231.xsd"/>
  </ix:references>

  <ix:resources>
    <!-- Contexts define the "who/when" of each fact -->
    <xbrli:context id="c_entity">
      <xbrli:entity>
        <xbrli:identifier scheme="http://www.sec.gov/CIK">0001234567</xbrli:identifier>
      </xbrli:entity>
      <xbrli:period>
        <xbrli:startDate>2024-01-01</xbrli:startDate>
        <xbrli:endDate>2024-12-31</xbrli:endDate>
      </xbrli:period>
    </xbrli:context>
    <xbrli:context id="c_instant_20241231">
      <xbrli:entity>
        <xbrli:identifier scheme="http://www.sec.gov/CIK">0001234567</xbrli:identifier>
      </xbrli:entity>
      <xbrli:period>
        <xbrli:instant>2024-12-31</xbrli:instant>
      </xbrli:period>
    </xbrli:context>

    <!-- Units for numeric facts -->
    <xbrli:unit id="USD">
      <xbrli:measure>iso4217:USD</xbrli:measure>
    </xbrli:unit>
    <xbrli:unit id="shares">
      <xbrli:measure>xbrli:shares</xbrli:measure>
    </xbrli:unit>
  </ix:resources>
</ix:header>

<!-- === VISIBLE DOCUMENT CONTENT === -->

<!-- Cover page with inline-tagged entity info -->
<div style="text-align:center;">
  <p style="font-size:14pt;font-weight:bold;">
    <ix:nonNumeric contextRef="c_entity" name="dei:EntityRegistrantName">
      ACME Corporation
    </ix:nonNumeric>
  </p>
  <p>Annual Report Pursuant to Section 13 of the Securities Exchange Act of 1934</p>
  <p>For the fiscal year ended
    <ix:nonNumeric contextRef="c_entity" name="dei:DocumentPeriodEndDate"
                   format="ixt:date-monthname-day-year-en">December 31, 2024</ix:nonNumeric>
  </p>
</div>

<!-- === NARRATIVE TEXT BLOCK (the key pattern for ESG extraction) === -->

<!-- Large textBlock wrapping an entire note disclosure -->
<ix:nonNumeric contextRef="c_entity"
               name="us-gaap:OrganizationConsolidationAndPresentationOfFinancialStatementsDisclosureTextBlock"
               id="f-note1"
               escape="true">
<div>
  <p style="font-size:10pt;font-weight:bold;font-family:'Times New Roman';">
    NOTE 1 - ORGANIZATION AND DESCRIPTION OF BUSINESS
  </p>
  <p style="font-size:10pt;font-family:'Times New Roman';">
    ACME Corporation (the "Company") was incorporated in Delaware in 2005.
    The Company designs, manufactures, and sells consumer electronics and
    related software services. The Company's principal markets include
    North America, Europe, and Asia-Pacific.
  </p>
  <p style="font-size:10pt;font-family:'Times New Roman';">
    The Company has assessed the impact of climate-related risks on its
    operations and supply chain. Physical risks including extreme weather
    events and transition risks from evolving regulations are monitored
    through the enterprise risk management framework.
  </p>
</div>
</ix:nonNumeric>

<!-- Numeric fact inline within text -->
<p>
  Total revenue for the year was $<ix:nonFraction contextRef="c_entity"
    name="us-gaap:Revenues" unitRef="USD" decimals="-6"
    format="ixt:num-dot-decimal" scale="6">42,300</ix:nonFraction> million.
</p>

<!-- Short string fact (not a textBlock) -->
<p>
  State of incorporation:
  <ix:nonNumeric contextRef="c_instant_20241231"
                 name="dei:EntityIncorporationStateCountryCode">DE</ix:nonNumeric>
</p>

</body>
</html>
```

### ESRS Sustainability Report (iXBRL) - Realistic Structure

```html
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
      xmlns:ixt="http://www.xbrl.org/inlineXBRL/transformation/2020-02-12"
      xmlns:xbrli="http://www.xbrl.org/2003/instance"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xmlns:link="http://www.xbrl.org/2003/linkbase"
      xmlns:esrs="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22"
      xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
      xml:lang="en">
<head>
  <title>EuroTech AG - ESRS Sustainability Statement 2025</title>
</head>
<body>

<ix:header>
  <ix:references>
    <link:schemaRef xlink:type="simple"
                    xlink:href="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_all.xsd"/>
  </ix:references>
  <ix:resources>
    <xbrli:context id="FY2025">
      <xbrli:entity>
        <xbrli:identifier scheme="http://standards.iso.org/iso/17442">529900EXAMPLE00LEI00</xbrli:identifier>
      </xbrli:entity>
      <xbrli:period>
        <xbrli:startDate>2025-01-01</xbrli:startDate>
        <xbrli:endDate>2025-12-31</xbrli:endDate>
      </xbrli:period>
    </xbrli:context>
    <xbrli:context id="FY2025_Scope1">
      <xbrli:entity>
        <xbrli:identifier scheme="http://standards.iso.org/iso/17442">529900EXAMPLE00LEI00</xbrli:identifier>
        <!-- Dimensional qualifier for Scope 1 -->
        <xbrli:segment>
          <xbrldi:explicitMember dimension="esrs:GHGCategoryAxis">esrs:Scope1Member</xbrldi:explicitMember>
        </xbrli:segment>
      </xbrli:entity>
      <xbrli:period>
        <xbrli:startDate>2025-01-01</xbrli:startDate>
        <xbrli:endDate>2025-12-31</xbrli:endDate>
      </xbrli:period>
    </xbrli:context>
    <xbrli:unit id="tCO2eq">
      <xbrli:measure>esrs:tCO2eq</xbrli:measure>
    </xbrli:unit>
  </ix:resources>
</ix:header>

<!-- ================================================================ -->
<!--  ESRS 2 - General Disclosures                                    -->
<!-- ================================================================ -->

<h1>ESRS 2 - General Disclosures</h1>

<!-- GOV-1: Role of administrative, management and supervisory bodies -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfRoleOfAdministrativeManagementAndSupervisoryBodiesExplanation"
               id="gov1-text"
               escape="true">
<div>
  <h2>GOV-1 - Role of administrative, management and supervisory bodies</h2>
  <p>The Supervisory Board of EuroTech AG has overall oversight of sustainability
  matters. A dedicated Sustainability Committee was established in 2023, meeting
  quarterly to review progress against ESG targets. The committee comprises three
  independent non-executive directors with expertise in climate science, social
  policy, and corporate governance.</p>
  <p>The Management Board member responsible for sustainability is the Chief
  Operating Officer, who reports to the full Management Board on sustainability
  performance at each monthly meeting. Key sustainability-related decisions,
  including the approval of the transition plan and science-based targets, require
  full Management Board approval.</p>
</div>
</ix:nonNumeric>

<!-- IRO-1: Description of process to identify material impacts, risks, opportunities -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DescriptionOfProcessToIdentifyAndAssessMaterialImpactsRisksAndOpportunities"
               id="iro1-text"
               escape="true">
<div>
  <h2>IRO-1 - Process to identify and assess material impacts, risks, and opportunities</h2>
  <p>EuroTech conducts a double materiality assessment annually, engaging both
  internal stakeholders (management, employees, internal audit) and external
  stakeholders (investors, customers, suppliers, civil society). The assessment
  follows EFRAG Implementation Guidance IG1, considering both impact materiality
  and financial materiality thresholds.</p>
  <p>The process involves:</p>
  <ul>
    <li>Identification of actual and potential impacts across the value chain</li>
    <li>Assessment of severity (scale, scope, irremediability) for negative impacts</li>
    <li>Assessment of financial effects (likelihood and magnitude) for risks and opportunities</li>
    <li>Stakeholder engagement through structured interviews and surveys</li>
  </ul>
</div>
</ix:nonNumeric>

<!-- ================================================================ -->
<!--  ESRS E1 - Climate Change                                        -->
<!-- ================================================================ -->

<h1>ESRS E1 - Climate Change</h1>

<!-- E1-1: Transition plan for climate change mitigation (Level 1 textBlock) -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfTransitionPlanForClimateChangeMitigationExplanation"
               id="e1-1-block"
               escape="true">
<div>
  <h2>E1-1 Transition plan for climate change mitigation</h2>

  <!-- Nested Level 2 child element: description of targets -->
  <ix:nonNumeric contextRef="FY2025"
                 name="esrs:DescriptionOfGHGEmissionReductionTargetsInTransitionPlan"
                 id="e1-1-targets"
                 escape="true">
  <p>EuroTech has committed to achieving net-zero greenhouse gas emissions across
  its value chain by 2050, with an interim target of 42% reduction in Scope 1 and
  2 emissions by 2030 (base year 2020). These targets have been validated by the
  Science Based Targets initiative (SBTi) as consistent with a 1.5C pathway.</p>
  </ix:nonNumeric>

  <!-- Level 2: description of decarbonisation levers -->
  <ix:nonNumeric contextRef="FY2025"
                 name="esrs:DescriptionOfDecarbonisationLeversAndKeyActionsPlanned"
                 id="e1-1-levers"
                 escape="true">
  <p>Key decarbonisation levers include:</p>
  <ul>
    <li>Transition of manufacturing facilities to 100% renewable electricity by 2028
    (currently 67% in 2025)</li>
    <li>Electrification of company vehicle fleet, targeting full EV transition by 2030</li>
    <li>Engagement with top 50 suppliers (representing 80% of Scope 3 emissions) to
    set their own science-based targets by 2027</li>
    <li>Investment of EUR 120 million in energy efficiency retrofits across production
    sites over 2025-2030</li>
  </ul>
  </ix:nonNumeric>

  <!-- Level 2: description of alignment with Paris Agreement -->
  <ix:nonNumeric contextRef="FY2025"
                 name="esrs:DescriptionOfCompatibilityOfTransitionPlanWithLimitingGlobalWarmingTo1Point5DegreesCelsius"
                 id="e1-1-paris"
                 escape="true">
  <p>The transition plan has been assessed against the IEA Net Zero Emissions by
  2050 Scenario (NZE) and the IPCC AR6 1.5C pathway with limited overshoot.
  The Company's emission reduction trajectory is consistent with a 1.5C-aligned
  carbon budget through 2050. An independent third-party verification of the
  plan's Paris-alignment was completed in Q3 2025.</p>
  </ix:nonNumeric>

  <!-- Boolean flag fact embedded in narrative context -->
  <p>The transition plan has been approved by the administrative, management, and
  supervisory bodies:
  <ix:nonNumeric contextRef="FY2025"
                 name="esrs:TransitionPlanHasBeenApprovedByAdministrativeManagementAndSupervisoryBodies"
                 format="ixt:fixed-true">Yes</ix:nonNumeric>
  </p>
</div>
</ix:nonNumeric>

<!-- E1-6: Gross Scope 1, 2, 3 GHG emissions (mixing narrative + numeric) -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfGrossScopes1And2And3AndTotalGHGEmissionsExplanation"
               id="e1-6-block"
               escape="true">
<div>
  <h2>E1-6 Gross Scopes 1, 2, 3 and total GHG emissions</h2>

  <p>EuroTech's total GHG emissions for the reporting period were:</p>
  <table>
    <tr>
      <td>Gross Scope 1 emissions</td>
      <td><ix:nonFraction contextRef="FY2025_Scope1"
                          name="esrs:GrossScope1GHGEmissions"
                          unitRef="tCO2eq" decimals="0">45,230</ix:nonFraction> tCO2eq</td>
    </tr>
  </table>

  <!-- Narrative describing methodology -->
  <ix:nonNumeric contextRef="FY2025"
                 name="esrs:DescriptionOfMethodologiesUsedForCalculatingGHGEmissions"
                 id="e1-6-methodology"
                 escape="true">
  <p>Emissions have been calculated in accordance with the GHG Protocol Corporate
  Accounting and Reporting Standard (revised edition). Scope 1 emissions are
  calculated using site-level fuel consumption data with emission factors from
  DEFRA 2025. The consolidation approach used is operational control.</p>
  </ix:nonNumeric>
</div>
</ix:nonNumeric>

<!-- ================================================================ -->
<!--  ESRS S1 - Own Workforce                                         -->
<!-- ================================================================ -->

<h1>ESRS S1 - Own Workforce</h1>

<!-- S1-1: Policies related to own workforce -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfPoliciesRelatedToOwnWorkforceExplanation"
               id="s1-1-block"
               escape="true">
<div>
  <h2>S1-1 Policies related to own workforce</h2>
  <p>EuroTech maintains comprehensive policies governing its relationship with
  its own workforce, including:</p>
  <ul>
    <li><strong>Human Rights Policy:</strong> Aligned with the UN Guiding Principles
    on Business and Human Rights and the ILO Declaration on Fundamental Principles
    and Rights at Work. Covers all employees, contractors, and temporary workers.</li>
    <li><strong>Diversity, Equity and Inclusion Policy:</strong> Sets targets for
    gender balance in leadership (40% women by 2027, currently 32%) and implements
    mandatory unconscious bias training.</li>
    <li><strong>Health and Safety Policy:</strong> Certified to ISO 45001 across all
    manufacturing sites. Targets zero fatalities and a Lost Time Injury Frequency
    Rate below 1.0.</li>
  </ul>
  <p>All workforce policies are reviewed annually by the Management Board and
  approved by the Supervisory Board's Sustainability Committee. The policies apply
  to all 28,500 employees across 14 countries of operation.</p>
</div>
</ix:nonNumeric>

<!-- ================================================================ -->
<!--  ESRS G1 - Business Conduct                                      -->
<!-- ================================================================ -->

<h1>ESRS G1 - Business Conduct</h1>

<!-- G1-1: Corporate culture and business conduct policies -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfCorporateCultureAndBusinessConductPoliciesExplanation"
               id="g1-1-block"
               escape="true">
<div>
  <h2>G1-1 Corporate culture and business conduct policies</h2>
  <p>The Company's Code of Conduct forms the foundation of its approach to
  business ethics. It covers anti-corruption and bribery, conflicts of interest,
  data protection, fair competition, and responsible tax practices. All employees
  must complete annual Code of Conduct training, with a 98.5% completion rate
  achieved in 2025.</p>
  <p>The Company maintains a confidential whistleblower mechanism accessible via
  a dedicated external hotline (operated by an independent third party) and a
  web-based reporting platform available in 12 languages. During 2025, 47 reports
  were received through these channels, all of which were investigated and
  resolved. No substantiated cases of corruption were identified.</p>
</div>
</ix:nonNumeric>

</body>
</html>
```

### The `ix:continuation` Pattern (for text spanning page breaks)

When a narrative block spans multiple pages or sections, `continuedAt` links fragments:

```html
<!-- First part of the disclosure -->
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfTransitionPlanForClimateChangeMitigationExplanation"
               id="e1-1-part1"
               escape="true"
               continuedAt="e1-1-part2">
<div>
  <h2>E1-1 Transition plan for climate change mitigation</h2>
  <p>EuroTech has committed to achieving net-zero greenhouse gas emissions
  across its value chain by 2050...</p>
</div>
</ix:nonNumeric>

<!-- Page break or other intervening content -->
<div style="page-break-before:always;"></div>

<!-- Continuation of the same fact -->
<ix:continuation id="e1-1-part2">
<div>
  <p>...with an interim target of 42% reduction by 2030. The transition plan
  was approved by the Supervisory Board on 15 March 2025.</p>
</div>
</ix:continuation>
```

### The `ix:exclude` Pattern (excluding boilerplate from fact value)

```html
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DescriptionOfDecarbonisationLeversAndKeyActionsPlanned"
               id="e1-1-levers"
               escape="true">
<div>
  <ix:exclude><p style="font-size:8pt;">Page 45 of 120</p></ix:exclude>
  <p>Key decarbonisation levers include transitioning to renewable energy...</p>
</div>
</ix:nonNumeric>
```

The page header "Page 45 of 120" is excluded from the extracted XBRL fact value but remains visible in the rendered HTML.

### The `ixt:fixed-empty` Pattern (disclosure indicator only)

For very large section-level text blocks where you want to mark "this section exists" without duplicating all content in the extracted XBRL:

```html
<ix:nonNumeric contextRef="FY2025"
               name="esrs:DisclosureOfTransitionPlanForClimateChangeMitigationExplanation"
               id="e1-1-indicator"
               format="ixt:fixed-empty">
<!-- The entire section content is here visually, but the extracted
     XBRL fact value is an empty string. This serves as a "disclosure
     indicator" — confirming the company has made this disclosure. -->
<div>
  <h2>E1-1 Transition plan for climate change mitigation</h2>
  <p>... 5 pages of detailed transition plan content ...</p>
</div>
</ix:nonNumeric>
```

---

## 4. Common Taxonomy Prefixes in ESG Reporting

### SEC / US-GAAP Ecosystem (for SEC climate disclosure rule)

| Prefix | Namespace | Usage |
|---|---|---|
| `us-gaap:` | `http://fasb.org/us-gaap/2024` | US GAAP financial concepts |
| `dei:` | `http://xbrl.sec.gov/dei/2024` | Document metadata (filer name, CIK, dates) |
| `srt:` | `http://fasb.org/srt/2024` | SEC Reporting Taxonomy (segment/geography) |
| `ecd:` | `http://xbrl.sec.gov/ecd/2024` | Executive compensation |
| `country:` | `http://xbrl.sec.gov/country/2024` | Country codes |

### ESRS / CSRD Ecosystem

| Prefix | Namespace | Usage |
|---|---|---|
| `esrs:` | `https://xbrl.efrag.org/taxonomy/esrs/2023-12-22` | All ESRS sustainability concepts |
| `xbrldi:` | `http://xbrl.org/2006/xbrldi` | Dimensional instance (for explicit/typed dimensions) |

### IFRS / ISSB Ecosystem

| Prefix | Namespace | Usage |
|---|---|---|
| `ifrs-full:` | `http://xbrl.ifrs.org/taxonomy/2024/ifrs-full` | IFRS accounting concepts |
| `ifrs-sds:` | `http://xbrl.ifrs.org/taxonomy/2024/ifrs-sds` | IFRS Sustainability Disclosure Standards (S1, S2) |

### GRI Ecosystem

| Prefix | Namespace | Usage |
|---|---|---|
| `gri:` | `http://xbrl.globalreporting.org/taxonomy/2025` | GRI Universal, Sector, Topic standards |

### Shared / Infrastructure

| Prefix | Namespace | Usage |
|---|---|---|
| `ix:` | `http://www.xbrl.org/2013/inlineXBRL` | Inline XBRL elements (v1.1) |
| `ixt:` | `http://www.xbrl.org/inlineXBRL/transformation/2020-02-12` | Transformation rules |
| `xbrli:` | `http://www.xbrl.org/2003/instance` | XBRL instance elements (context, unit) |
| `link:` | `http://www.xbrl.org/2003/linkbase` | Taxonomy linkbase references |
| `xlink:` | `http://www.w3.org/1999/xlink` | XLink (for schemaRef) |
| `iso4217:` | `http://www.xbrl.org/2003/iso4217` | Currency codes |
| `dtr-types:` | `http://www.xbrl.org/dtr/type/2022-03-31` | Data Type Registry (textBlockItemType, etc.) |

---

## 5. ESRS Taxonomy Element Name Examples

These are derived from EFRAG's taxonomy files and documentation. The `esrs:` prefix is used throughout.

### ESRS 2 - General Disclosures (Cross-cutting)

```
esrs:DisclosureOfRoleOfAdministrativeManagementAndSupervisoryBodiesExplanation
esrs:DisclosureOfInformationAboutSustainabilityDueDiligenceExplanation
esrs:DescriptionOfProcessToIdentifyAndAssessMaterialImpactsRisksAndOpportunities
esrs:DisclosureOfPoliciesAdoptedToManageMaterialSustainabilityMattersExplanation
esrs:DisclosureOfActionsAndResourcesInRelationToMaterialSustainabilityMattersExplanation
esrs:DisclosureOfNatureScaleAndScopeOfSignificantRisksAndOpportunitiesExplanation
```

### ESRS E1 - Climate Change

```
esrs:DisclosureOfTransitionPlanForClimateChangeMitigationExplanation
esrs:DescriptionOfGHGEmissionReductionTargetsInTransitionPlan
esrs:DescriptionOfDecarbonisationLeversAndKeyActionsPlanned
esrs:DescriptionOfCompatibilityOfTransitionPlanWithLimitingGlobalWarmingTo1Point5DegreesCelsius
esrs:TransitionPlanHasBeenApprovedByAdministrativeManagementAndSupervisoryBodies
esrs:DisclosureOfPoliciesRelatedToClimateChangeMitigationAndAdaptationExplanation
esrs:DisclosureOfActionsAndResourcesInRelationToClimateChangePoliciesExplanation
esrs:DisclosureOfTargetsRelatedToClimateChangeMitigationAndAdaptationExplanation
esrs:DisclosureOfEnergyConsumptionAndMixExplanation
esrs:DisclosureOfGrossScopes1And2And3AndTotalGHGEmissionsExplanation
esrs:DescriptionOfMethodologiesUsedForCalculatingGHGEmissions
esrs:GrossScope1GHGEmissions
esrs:GrossScope2GHGEmissions
esrs:GrossScope3GHGEmissions
esrs:TotalGHGEmissions
esrs:DisclosureOfGHGRemovalsAndGHGMitigationProjectsFinancedThroughCarbonCreditsExplanation
esrs:DisclosureOfInternalCarbonPricingExplanation
esrs:DisclosureOfAnticipatedFinancialEffectsFromMaterialPhysicalAndTransitionRisksExplanation
```

### ESRS S1 - Own Workforce

```
esrs:DisclosureOfPoliciesRelatedToOwnWorkforceExplanation
esrs:DisclosureOfEngagementProcessesWithOwnWorkforceExplanation
esrs:DisclosureOfProcessesToRemediateNegativeImpactsOnOwnWorkforceExplanation
esrs:DisclosureOfCharacteristicsOfOwnWorkforceExplanation
esrs:DisclosureOfAdequateWagesExplanation
esrs:DisclosureOfWorkLifeBalanceExplanation
esrs:DisclosureOfHealthAndSafetyExplanation
esrs:DisclosureOfDiversityMetricsExplanation
esrs:DisclosureOfIncidentsOfDiscriminationAndCorrectiveActionsTakenExplanation
```

### ESRS G1 - Business Conduct

```
esrs:DisclosureOfCorporateCultureAndBusinessConductPoliciesExplanation
esrs:DisclosureOfManagementOfRelationshipsWithSuppliersExplanation
esrs:DisclosureOfPreventionAndDetectionOfCorruptionAndBriberyExplanation
esrs:DisclosureOfConfirmedIncidentsOfCorruptionOrBriberyExplanation
esrs:DisclosureOfPoliticalInfluenceAndLobbyingActivitiesExplanation
esrs:DisclosureOfPaymentPracticesExplanation
```

### Dimensional Axes (for disaggregation)

```
esrs:GHGCategoryAxis                       (Scope1Member, Scope2LocationBasedMember, etc.)
esrs:CountryAxis                            (explicit dimension)
esrs:GenderAxis                             (FemaleMember, MaleMember, OtherGenderMember)
esrs:IdentifierOfPolicyTypedAxis            (typed dimension, entity-specific)
esrs:IdentifierOfTargetTypedAxis            (typed dimension, entity-specific)
esrs:IdentifierOfActionPlanTypedAxis        (typed dimension, entity-specific)
esrs:IdentifierOfImpactRiskAndOpportunityTypedAxis
```

### Cross-reference Elements (linking disclosures)

```
esrs:IdentifiersOfRelatedImpactsRisksAndOpportunities
esrs:IdentifiersOfRelatedTargets
esrs:IdentifiersOfRelatedPolicies
esrs:IdentifiersOfRelatedActionPlans
```

---

## 6. Implications for RAI Indicator Extraction

### What to Parse

For extracting textual RAI indicators from XBRL documents:

1. **Primary targets:** `ix:nonNumeric` elements where the `name` attribute references a `TextBlock` or `Explanation` concept (these contain the narrative disclosures).

2. **Key attributes to capture:**
   - `name` -- the taxonomy concept (e.g., `esrs:DisclosureOfTransitionPlanForClimateChangeMitigationExplanation`)
   - `contextRef` -- links to the context (reporting entity + period)
   - `id` -- unique fact identifier
   - `escape` -- whether HTML is preserved (`true`) or stripped (`false`)
   - `continuedAt` -- if the text continues in another fragment

3. **Nested facts:** `ix:nonNumeric` elements can be nested. A Level 1 parent textBlock contains Level 2 child elements. Both parent and children are independently extractable facts.

4. **Exclusions:** Content within `ix:exclude` tags should be stripped. Content in `ix:hidden` is metadata, not displayed narrative.

5. **Data type check:** The taxonomy concept's type determines interpretation:
   - `textBlockItemType` --> rich HTML narrative (use `escape="true"`)
   - `stringItemType` --> plain text
   - `booleanItemType` --> Yes/No flag

### Extraction Strategy

```
For each ix:nonNumeric element in the document:
  1. Read the "name" attribute to get the taxonomy concept
  2. Map concept to the relevant ESRS/GRI/IFRS disclosure requirement
  3. Check if concept is narrative (textBlock/Explanation suffix)
  4. If escape="true", extract inner HTML as the fact value
  5. If escape="false", extract text-only content
  6. Follow continuedAt chains to reconstruct full text
  7. Strip ix:exclude content
  8. Record contextRef for entity/period metadata
```

---

## Sources

- [EDGAR XBRL Guide (SEC, Jan 2026)](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)
- [Inline XBRL Part 1: Specification 1.1](https://www.xbrl.org/specification/inlinexbrl-part1/rec-2013-11-18/inlinexbrl-part1-rec-2013-11-18.html)
- [Designing HTML for Inline XBRL 1.0](https://www.xbrl.org/WGN/html-for-ixbrl-wgn/WGN-2023-04-19/html-for-ixbrl-wgn-2023-04-19.html)
- [Inline XBRL Block Tagging 1.0](https://www.xbrl.org/WGN/blocktagging-wgn/WGN-2024-06-18/blocktagging-wgn-2024-06-18.html)
- [EFRAG ESRS XBRL Taxonomy](https://www.efrag.org/en/sustainability-reporting/esrs-workstreams/digital-reporting-with-xbrl)
- [ESRS Set 1 XBRL Taxonomy Explanatory Note](https://xbrl.efrag.org/downloads/ESRS-Set1-XBRL-Taxonomy-Explanatory-Note-and-Basis-for-Conclusions.pdf)
- [IFRS Sustainability Disclosure Taxonomy 2024](https://www.ifrs.org/projects/completed-projects/2024/ifrs-sustainability-disclosure-taxonomy/)
- [GRI Sustainability Taxonomy](https://www.globalreporting.org/standards/gri-sustainability-taxonomy/)
- [XBRL US - Supporting ESG with Standards](https://xbrl.us/research/supporting-esg-with-standards/)
- [Briink - Digitizing the ESRS](https://www.briink.com/post/digitizing-the-esrs-the-xbrl-taxonomy-and-machine-readable-sustainability-reporting)
- [SEC Inline XBRL Overview](https://www.sec.gov/data-research/structured-data/inline-xbrl)
