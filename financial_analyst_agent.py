from crewai import Agent
from crewai_tools import SerperDevTool
from llm_config import get_llm


def create_business_financial_analyst():
    return Agent(
        role="Business and Financial Analyst",
        goal=(
            "Translate research findings into business implications, business-model considerations, "
            "economic drivers, KPI requirements, cost and revenue considerations, and capability needs."
        ),
        backstory=(
            "You are a strategy and business-finance analyst. You reason from available evidence, "
            "avoid inventing company financials, and explicitly label estimates, assumptions, and "
            "data gaps. You use web research when a current external benchmark is necessary."
        ),
        tools=[SerperDevTool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
