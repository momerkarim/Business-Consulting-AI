from crewai import Crew, Process

from engagement_agent import create_engagement_manager
from industry_research_agent import create_industry_researcher
from customer_analyst_agent import create_customer_analyst
from competitor_analyst_agent import create_competitor_analyst
from financial_analyst_agent import create_business_financial_analyst
from strategy_consultant_agent import create_strategy_consultant
from report_writer_agent import create_report_writer
from tasks import create_tasks


def build_crew():
    """Build the seven-agent consulting crew."""
    agents = [
        create_engagement_manager(),
        create_industry_researcher(),
        create_customer_analyst(),
        create_competitor_analyst(),
        create_business_financial_analyst(),
        create_strategy_consultant(),
        create_report_writer(),
    ]

    tasks = create_tasks(agents)

    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
    )
