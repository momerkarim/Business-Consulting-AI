from crewai import Agent
from llm_config import get_llm
from research_tools import get_web_search_tool


def create_competitor_analyst():
    return Agent(
        role="Competitive Intelligence Analyst",
        goal=(
            "Identify relevant direct and indirect competitors and analyze their products, "
            "positioning, pricing where publicly available, channels, capabilities, and differentiation."
        ),
        backstory=(
            "You are a competitive intelligence specialist. You compare competitors using "
            "documented evidence, distinguish facts from interpretation, and identify gaps or "
            "white spaces relevant to the client's business challenge."
        ),
        tools=[get_web_search_tool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
