from crewai import Task


def create_tasks(agents):
    (
        engagement_manager,
        industry_researcher,
        customer_analyst,
        competitor_analyst,
        financial_analyst,
        strategy_consultant,
        report_writer,
    ) = agents

    engagement_task = Task(
        description="""
You are starting a consulting engagement.

Client:
- Company: {company}
- Industry: {industry}
- Country/Market: {country}
- Business challenge: {challenge}
- Business objective: {objective}
- Additional context: {additional_context}

Create a consulting engagement brief containing:
1. Business context
2. Problem statement
3. Primary objective
4. Scope
5. Key research questions
6. Important assumptions
7. Decision criteria that later strategy options should be evaluated against

Do not invent company facts that the client did not provide.
""",
        expected_output="A structured consulting engagement brief.",
        agent=engagement_manager,
    )

    industry_task = Task(
        description="""
Using the engagement brief, research the current industry and market.

Investigate:
- Industry structure
- Market size or credible market indicators
- Growth trends
- Major industry trends
- Technology trends
- Regulatory or policy factors where relevant
- Macro-economic factors where relevant
- Major opportunities and threats

Use current web sources. For material claims, provide source name, URL, and publication date/year when available.
Distinguish verified information from estimates and interpretation.
""",
        expected_output="An evidence-based industry research report with source references.",
        agent=industry_researcher,
        context=[engagement_task],
    )

    customer_task = Task(
        description="""
Using the engagement brief and relevant industry findings, analyze the market and customer.

Investigate:
- Relevant customer segments
- Target customer characteristics
- Customer needs and pain points
- Adoption or purchase drivers
- Unmet needs
- Customer behavior or digital behavior where relevant
- Market demand signals
- Implications for the client's value proposition

Use current web sources where useful. Clearly label assumptions and avoid inventing customer statistics.
""",
        expected_output="A customer and market analysis with source references and business implications.",
        agent=customer_analyst,
        context=[engagement_task, industry_task],
    )

    competitor_task = Task(
        description="""
Using the engagement brief and industry findings, perform competitive intelligence.

Identify:
- Direct competitors
- Indirect/substitute competitors
- Products/services
- Target segments
- Pricing or commercial model where publicly available
- Distribution/channel approach
- Positioning
- Documented differentiators
- Strengths and weaknesses supported by evidence
- Potential market gaps or white spaces

Do not make unsupported claims about competitor weaknesses.
Include source references for material current facts.
""",
        expected_output="A structured competitive landscape and comparison with source references.",
        agent=competitor_analyst,
        context=[engagement_task, industry_task, customer_task],
    )

    financial_task = Task(
        description="""
Translate the engagement and research findings into business and financial implications.

Analyze:
- Business model implications
- Revenue drivers
- Cost drivers
- Unit-economic considerations
- Required capabilities
- Operating-model implications
- Key KPIs
- Potential value pools
- Financial assumptions and data gaps
- External benchmarks if they are relevant and can be sourced

Do not fabricate company financial figures. Clearly label estimates and assumptions.
""",
        expected_output="A business and financial implications analysis with assumptions and KPIs.",
        agent=financial_analyst,
        context=[engagement_task, industry_task, customer_task, competitor_task],
    )

    strategy_task = Task(
        description="""
Develop the strategic analysis using all previous findings.

Produce:
1. SWOT analysis
2. Strategic themes
3. 3-4 plausible strategic options
4. Trade-offs for each option
5. Risks and mitigations
6. Capability requirements
7. Recommended sequencing or phased approach
8. 90-day, 6-month, and 12-24 month implementation roadmap
9. Suggested KPIs

Evaluate options against explicit criteria from the engagement brief. Explain the evidence and assumptions behind each assessment.
""",
        expected_output="A structured strategic options analysis and implementation roadmap.",
        agent=strategy_consultant,
        context=[engagement_task, industry_task, customer_task, competitor_task, financial_task],
    )

    report_task = Task(
        description="""
Act as the final consulting partner.

Using every prior task output, create the final business strategy report.

Required structure:
# Business Strategy Report
## 1. Executive Summary
## 2. Business Context and Problem
## 3. Consulting Scope and Key Questions
## 4. Industry Analysis
## 5. Market and Customer Analysis
## 6. Competitive Landscape
## 7. Business and Financial Implications
## 8. SWOT Analysis
## 9. Strategic Options and Trade-offs
## 10. Strategic Direction and Priorities
## 11. Implementation Roadmap
## 12. KPIs and Measurement
## 13. Risks and Mitigations
## 14. Assumptions, Data Gaps and Limitations
## 15. Sources

Important editorial rules:
- Do not invent facts, figures, sources, URLs, or citations.
- Separate facts, analysis, assumptions, and recommendations.
- Preserve source attribution for material external claims.
- If two research findings conflict, explicitly identify the conflict and explain which evidence appears more reliable.
- If evidence is insufficient, say so.
- Make the report useful for an executive audience.
- Do not claim that the report is a substitute for professional due diligence.
""",
        expected_output="A polished executive-ready business strategy report in Markdown.",
        agent=report_writer,
        context=[
            engagement_task,
            industry_task,
            customer_task,
            competitor_task,
            financial_task,
            strategy_task,
        ],
    )

    return [
        engagement_task,
        industry_task,
        customer_task,
        competitor_task,
        financial_task,
        strategy_task,
        report_task,
    ]
