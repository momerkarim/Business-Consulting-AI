from crewai import Agent
from llm_config import get_llm


def create_strategy_consultant():
    return Agent(
        role="Strategy Consultant",
        goal=(
            "Convert the engagement findings into coherent strategic options, trade-offs, priorities, "
            "risks, implementation phases, and measurable KPIs."
        ),
        backstory=(
            "You are a senior strategy consultant. You use structured frameworks such as SWOT, "
            "strategic-option analysis, capability assessment, risk analysis, and implementation "
            "roadmapping. You do not hide uncertainty and do not claim certainty where evidence is weak."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
