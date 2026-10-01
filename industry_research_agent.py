from crewai import Agent
from llm_config import get_llm
from research_tools import get_web_search_tool


def create_industry_researcher():
    return Agent(
        role="Industry Research Analyst",
        goal=(
            "Research the relevant industry and market using current online sources and produce "
            "evidence-based findings that directly address the consulting questions."
        ),
        backstory=(
            "You are an experienced market intelligence analyst. You investigate market structure, "
            "growth, trends, regulation, technology, macro factors, and industry economics. "
            "You never present an unsupported estimate as a verified fact."
        ),
        tools=[get_web_search_tool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
